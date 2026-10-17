# StudySpace — Your Personal AI Study Buddy

**Learn smarter. Stay organised. See your progress.**

StudySpace is a local-first study dashboard that combines study-material import, AI-generated notes, quizzes and flashcards, a focus timer, assignment tracking, exam dates and a score graph — powered by open-source LLMs through **OpenRouter**.

## What works in this version

-   **Document import:** TXT, Markdown, CSV, text-based PDF, DOCX and PPTX files.
-   **OpenRouter open-source study kits:** sends extracted text to state-of-the-art open-source LLMs (such as Meta Llama 3.3 70B, Llama 3.1 8B, Qwen 2.5, Gemma 2, and Mistral) via OpenRouter to generate structured notes, multiple-choice questions and flashcards.
-   **Interactive quiz:** choose an answer, receive immediate visual feedback, explanations, and navigate through questions.
-   **Flashcards:** click to flip cards and reveal answers with previous/next card navigation.
-   **Focus timer:** start, pause, resume and reset a 25-minute Pomodoro session with an active progress bar.
-   **Assignments and exams:** add, complete, and delete assignments; add and track exam dates with dynamic countdowns.
-   **Progress graph:** log quiz/test marks and visualize improvement over time on an SVG performance chart.
-   **Local persistence:** assignments, exams, focus time, results, OpenRouter preferences, and generated study kits are saved in browser `localStorage`.
-   **Responsive interface:** adapts smoothly across desktop, tablet, and mobile screens.

## Requirements

-   Windows, macOS or Linux
-   Python 3.10 or newer
-   An [OpenRouter API key](https://openrouter.ai/keys)
-   A modern browser

## Run on Windows (PowerShell)

### 1. Put the files in one folder

```text
studyspace/
├── studyspace_dashboard.html
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```

### 2. Install Python dependencies

Open PowerShell in the project folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell execution policy blocks activation script, you can use the venv Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Configure your OpenRouter API key

Create a `.env` file in the project folder (or copy from `.env.example`):

```powershell
Copy-Item .env.example .env
```

Open `.env` and paste your OpenRouter key:

```ini
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct
```

> **Tip:** You can also configure or change your OpenRouter API key and preferred model directly inside the StudySpace web UI by clicking the **⚙ OpenRouter** button in the top bar!

### 4. Start StudySpace

Run:

```powershell
python app.py
```

Or using the virtualenv python:

```powershell
.\.venv\Scripts\python.exe app.py
```

Open **http://127.0.0.1:5000** in your browser.

### 5. Generate a study kit

1.  Upload a supported study file (PDF, DOCX, PPTX, TXT, MD, CSV) via file picker or drag-and-drop.
2.  Wait for the import notification confirming text extraction.
3.  Click **✦ Generate with OpenRouter**.
4.  Review Notes, Quiz questions, and Flashcards!

## Recommended Open-Source Models on OpenRouter

You can choose any open-source model available on OpenRouter via `.env` or in the in-app **⚙ OpenRouter** settings modal:

| Model ID | Provider | Description |
| :--- | :--- | :--- |
| `meta-llama/llama-3.3-70b-instruct` | Meta | **Default & Recommended.** State-of-the-art open weights model. Excellent JSON structuring and reasoning. |
| `meta-llama/llama-3.1-8b-instruct:free` | Meta | Free tier open-source model on OpenRouter. Fast and lightweight. |
| `qwen/qwen-2.5-72b-instruct` | Qwen / Alibaba | High accuracy and exceptional structured JSON adherence. |
| `google/gemma-2-9b-it:free` | Google | Google open weights Gemma model available on free tier. |
| `mistralai/mistral-small-24b-instruct-2501` | Mistral AI | Balanced, efficient open-weights model. |

To change the model via environment variable:

```powershell
$env:OPENROUTER_MODEL = "qwen/qwen-2.5-72b-instruct"
python app.py
```

## File support and limits

-   Supported formats: `.txt`, `.md`, `.csv`, `.pdf`, `.docx`, `.pptx`.
-   Maximum upload size: 12 MB per file.
-   At most 24,000 extracted characters are sent to the model per study-kit request.
-   Scanned/image-only PDFs require OCR (not included in this lightweight version; PDFs must contain selectable text).
-   Older binary `.doc` and `.ppt` files are not supported; convert to modern DOCX/PPTX first.
-   Browser `localStorage` is local to the device/browser.

## Project structure

```text
studyspace/
├── studyspace_dashboard.html  # Frontend UI, styles and interactive study widgets
├── app.py                     # Flask backend, document parser and OpenRouter API client
├── requirements.txt           # Python dependencies (Flask, pypdf, python-docx, python-pptx, python-dotenv)
├── .env.example               # Configuration template for OpenRouter API key & model
└── README.md                  # Project setup and documentation
```
