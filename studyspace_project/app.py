"""Local API for StudySpace: document extraction + Ollama/Gemma study-kit generation."""
from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "studyspace_dashboard.html"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma4")
MAX_UPLOAD_BYTES = 12 * 1024 * 1024
MAX_SOURCE_CHARS = 24_000
ALLOWED_EXTENSIONS = {"txt", "md", "csv", "pdf", "docx", "pptx"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES


def extract_text(filename: str, raw: bytes) -> str:
    ext = Path(filename).suffix.lower()
    if ext not in {f".{x}" for x in ALLOWED_EXTENSIONS}:
        raise ValueError("Supported formats are TXT, MD, CSV, PDF, DOCX and PPTX.")
    if ext in {".txt", ".md", ".csv"}:
        text = raw.decode("utf-8-sig", errors="replace")
    elif ext == ".pdf":
        from pypdf import PdfReader
        import io
        reader = PdfReader(io.BytesIO(raw))
        text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
    elif ext == ".docx":
        from docx import Document
        import io
        doc = Document(io.BytesIO(raw))
        chunks = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                chunks.append(" | ".join(cell.text.strip() for cell in row.cells))
        text = "\n".join(chunks)
    else:  # .pptx
        from pptx import Presentation
        import io
        deck = Presentation(io.BytesIO(raw))
        slides = []
        for number, slide in enumerate(deck.slides, start=1):
            parts = [shape.text for shape in slide.shapes if getattr(shape, "has_text_frame", False) and shape.text.strip()]
            if parts:
                slides.append(f"Slide {number}\n" + "\n".join(parts))
        text = "\n\n".join(slides)
    text = text.strip()
    if not text:
        raise ValueError("No selectable text was found. Scanned/image-only PDFs need OCR, which this version does not include.")
    return text[:MAX_SOURCE_CHARS]


def call_ollama(prompt: str) -> dict:
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False, "format": "json", "options": {"temperature": 0.2}}
    req = Request(f"{OLLAMA_URL}/api/generate", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"Ollama returned HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError("Cannot connect to Ollama. Open Ollama and confirm it is running at http://127.0.0.1:11434.") from exc
    except TimeoutError as exc:
        raise RuntimeError("Ollama took too long. Try a shorter file or a smaller model.") from exc
    response_text = result.get("response", "")
    try:
        return json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("The model response was not valid JSON. Try generating again or use a different Gemma model.") from exc


@app.get("/")
def index():
    return send_from_directory(BASE_DIR, HTML_FILE.name)


@app.get("/api/health")
def health():
    try:
        req = Request(f"{OLLAMA_URL}/api/tags", method="GET")
        with urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode("utf-8"))
        models = [m.get("name", "") for m in data.get("models", [])]
        installed = any(m == OLLAMA_MODEL or m.startswith(OLLAMA_MODEL + ":") for m in models)
        return jsonify(ok=True, ollama=True, model=OLLAMA_MODEL, model_installed=installed, available_models=models)
    except Exception as exc:
        return jsonify(ok=False, ollama=False, model=OLLAMA_MODEL, error=str(exc)), 200


@app.post("/api/upload")
def upload():
    uploaded = request.files.get("file")
    if uploaded is None or not uploaded.filename:
        return jsonify(error="Choose a file to upload."), 400
    filename = secure_filename(uploaded.filename)
    try:
        text = extract_text(filename, uploaded.read())
        return jsonify(filename=filename, text=text, characters=len(text))
    except (ValueError, ImportError) as exc:
        return jsonify(error=str(exc)), 400
    except Exception as exc:
        app.logger.exception("Document extraction failed")
        return jsonify(error=f"Could not extract this document: {exc}"), 500


@app.post("/api/generate-study-kit")
def generate_study_kit():
    body = request.get_json(silent=True) or {}
    source = str(body.get("text", "")).strip()[:MAX_SOURCE_CHARS]
    filename = str(body.get("filename", "study material"))[:160]
    if len(source) < 40:
        return jsonify(error="Upload a document with at least 40 characters of readable text."), 400
    prompt = f'''You are StudySpace, a careful study assistant. Create a useful study kit ONLY from the source text below. Do not invent facts. If a detail is unclear, avoid testing it.
Return ONLY a JSON object with exactly these keys:
- "notes": array of 5 to 8 objects, each with "title" and "content" strings.
- "quiz": array of 5 multiple-choice questions. Each has "question" string, "options" array of exactly 4 strings, "answer" integer index 0-3, and "explanation" string.
- "flashcards": array of 6 to 10 objects, each with "front" and "back" strings.
Make the questions test different key concepts. Ensure every answer index is correct. Use concise, clear language. Do not include markdown fences.

SOURCE FILE: {filename}
SOURCE TEXT:
{source}'''
    try:
        kit = call_ollama(prompt)
        for key in ("notes", "quiz", "flashcards"):
            if not isinstance(kit.get(key), list) or not kit[key]:
                raise RuntimeError(f"Model output is missing a valid '{key}' list.")
        return jsonify(study_kit=kit, model=OLLAMA_MODEL)
    except RuntimeError as exc:
        return jsonify(error=str(exc)), 502
    except Exception as exc:
        app.logger.exception("Study-kit generation failed")
        return jsonify(error=f"Study-kit generation failed: {exc}"), 500


@app.errorhandler(413)
def too_large(_error):
    return jsonify(error="File is too large. The maximum upload size is 12 MB."), 413


if __name__ == "__main__":
    print(f"StudySpace is starting. Ollama URL: {OLLAMA_URL}; model: {OLLAMA_MODEL}")
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
