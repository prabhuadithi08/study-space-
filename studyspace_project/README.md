# StudySpace — Your Personal AI Study Buddy

**Learn smarter. Stay organised. See your progress.**

StudySpace is a local-first study dashboard that combines study-material
import, AI-generated notes, quizzes and flashcards, a focus timer,
assignment tracking, exam dates and a score graph.

## What works in this version

-   **Document import:** TXT, Markdown, CSV, text-based PDF, DOCX and
    PPTX files.
-   **Gemma study kits:** sends extracted text to a local Ollama model
    and requests structured notes, multiple-choice questions and
    flashcards.
-   **Interactive quiz:** choose an answer, receive feedback, and move
    through generated questions.
-   **Flashcards:** flip cards to reveal answers and move between cards.
-   **Focus timer:** start, pause and reset a 25-minute session.
-   **Assignments and exams:** add, complete, and delete assignments;
    add and delete exam dates.
-   **Progress graph:** add quiz/test scores and view them over time.
-   **Local persistence:** assignments, exams, focus time, results and
    the latest study kit are stored in the browser's local storage.
-   **Responsive interface:** adapts to desktop and mobile screens.

AI features require the Python backend, Ollama and a compatible model.
The app has been wired for this workflow, but you should run the setup
below and test generation on your own computer before presenting it as a
verified end-to-end demo.

## Requirements

-   Windows, macOS or Linux
-   Python 3.10 or newer
-   [Ollama](https://ollama.com/download)
-   A Gemma model available in your Ollama installation
-   A modern browser

## Run on Windows (PowerShell)

### 1. Put the files in one folder

Keep these files together:

``` text
studyspace/
├── studyspace_dashboard.html
├── app.py
├── requirements.txt
└── README.md
```

### 2. Install Python dependencies

Open PowerShell in the project folder and run:

``` powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, you can skip activation and use the
venv Python directly:

``` powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Start Ollama and download the model

Open Ollama, then in PowerShell run:

``` powershell
ollama --version
ollama pull gemma4
ollama run gemma4
```

If `ollama` is not recognised, install Ollama for Windows from the
official link above, finish installation, close and reopen PowerShell,
and try `ollama --version` again. If your installed model has a
different name, use that exact name in the commands and in the
configuration below.

Exit the interactive model prompt when you have confirmed it runs. Leave
Ollama running in the background.

### 4. Start StudySpace

In a second PowerShell window, navigate to the project folder, activate
the environment if needed, and run:

``` powershell
python app.py
```

Open **http://127.0.0.1:5000** in your browser. Do not double-click the
HTML file for AI features; the app needs to be served by `app.py` so the
browser can call its local API.

### 5. Generate a study kit

1.  Upload a supported study file.
2.  Wait for the import message to confirm readable text was extracted.
3.  Select **Generate with Gemma**.
4.  Review Notes, Quiz and Flashcards. Verify important details against
    your original source.

## Configure a different Ollama model

The default model is `gemma4`. If your model uses a different tag, set
`OLLAMA_MODEL` before starting the server:

``` powershell
$env:OLLAMA_MODEL = "your-installed-model-tag"
python app.py
```

You can also change the Ollama server address with `OLLAMA_URL` if you
have configured Ollama somewhere other than `http://127.0.0.1:11434`.

## File support and limits

-   Supported: `.txt`, `.md`, `.csv`, `.pdf`, `.docx`, `.pptx`.
-   Maximum upload size: 12 MB per file.
-   At most 24,000 extracted characters are sent to the model per
    study-kit request.
-   Scanned/image-only PDFs are not OCR-processed; the PDF must contain
    selectable text.
-   Older `.doc` and `.ppt` files are not supported. Save them as
    DOCX/PPTX first.
-   Local storage is specific to the browser and device. This is not a
    multi-user app and has no cloud account or cross-device sync.
-   The graph starts with example scores to demonstrate the UI. Remove
    or replace them before a real presentation if you want to show only
    your own results.
-   AI-generated content can be incorrect or incomplete. Always check it
    against the uploaded material.

## Project structure

``` text
studyspace/
├── studyspace_dashboard.html  # Frontend, styles and browser interactions
├── app.py                     # Flask API, document extraction and Ollama requests
├── requirements.txt           # Python dependencies
└── README.md                  # Setup and project documentation
```

## Troubleshooting

**`ollama` is not recognised:** install/reopen the terminal as described
above. Check `ollama --version` before proceeding.

**Ollama is reachable but the model is missing:** run `ollama list`,
then pull the model tag you want. If it is not named `gemma4`, set
`OLLAMA_MODEL` to the exact tag.

**Import fails:** confirm that `python app.py` is running, use one of
the supported file types, and keep the file under 12 MB. For PDFs, check
that you can select/copy the text in a PDF viewer.

**Generation fails:** run `ollama run gemma4` (or your configured model)
to confirm it works, try a smaller text file, and check the message
shown below the upload area.

## Hackathon demo checklist

-   [ ] Run the app on the presentation computer and generate a kit from
    a real sample document.
-   [ ] Verify the model tag and make sure Ollama has downloaded the
    model before the demo.
-   [ ] Replace the sample chart results with real demo scores, or
    clearly label them as sample data.
-   [ ] Capture screenshots or a short demo video after confirming the
    live workflow.
-   [ ] Explain that data is stored locally and that AI output should be
    checked against source material.

## Project vision

StudySpace aims to make studying feel less fragmented by bringing
learning resources, focused sessions, planning and progress tracking
into one cohesive workspace.

**StudySpace — Built to make every study session count.**
