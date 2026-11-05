# 🐍 Python Learning Chatbot

An interactive **local AI-powered Python tutor** built with [Streamlit](https://streamlit.io/) and [Ollama](https://ollama.com/), using the `llama3.2` model. Students can study Python concepts, ask questions, practice coding, take five-question MCQ quizzes, and upload their own study materials for context-aware explanations.

## Features

- **25 Python learning categories**, from fundamentals and data types to OOP, regular expressions, databases, algorithms, and projects.
- **Six learning modes**: Explain Concept, Explain Simply, Show Python Code, Give an Example, Practice, and Quiz.
- **Optional automatic lessons** when selecting a topic, with examples, expected output, common mistakes, and practice questions.
- **Five-question multiple-choice quizzes** with a hidden answer key and answer checking through the chat box.
- **Faculty-material uploads**: `.pdf`, `.pptx`, `.docx`, and `.txt`.
- **Keyword-based retrieval** of relevant passages from the uploaded material to support AI answers.
- **Chat history for the current Streamlit session** and controls to clear chat or remove uploaded material.

> **Important:** The AI runs through **your own Ollama installation**. This repository does not include model weights or a hosted AI server. It will not work by opening `app.py` in a browser or by publishing the files to GitHub Pages.

## Requirements

- Python 3.10 or newer (a current supported Python version is recommended).
- Ollama installed and running locally.
- Enough free memory and disk space for the `llama3.2` model.

## Quick start

### 1. Download or clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Python_Learning_Chatbot.git
cd Python_Learning_Chatbot
```

Alternatively, download the repository files as a ZIP, extract them, and open a terminal in the extracted project folder.

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install and start Ollama

Get Ollama from [ollama.com/download](https://ollama.com/download). In a terminal, download the model:

```bash
ollama pull llama3.2
```

Make sure Ollama is running. On systems where it does not start automatically, run `ollama serve` in another terminal.

### 5. Start the chatbot

```bash
streamlit run app.py
```

Open the local URL shown in the terminal (typically `http://localhost:8501`).

## How to use

1. Click **Choose Topic** in the left sidebar and select a category and subtopic.
2. Optionally enable **Automatically show lesson** to generate a lesson for the selection.
3. Select a learning mode and ask a question in the chat box.
4. In **Quiz** mode, request a quiz, then submit all five answers, for example `1=A, 2=B, 3=C, 4=D, 5=A`. The app scores your submission against the generated answer key.
5. Upload your own study material in the **Faculty Study Material** sidebar section to help guide explanations. Remove it when finished.

### About uploaded materials

Uploaded material is converted to text and stored in the current Streamlit session. When processing a file, the app creates a temporary file and deletes it after extraction. Relevant passages are sent to **your configured Ollama server** as part of prompts. The app uses **simple keyword matching**, not vector embeddings, and scanned/image-only documents are not supported by its text extraction.

For privacy and copyright reasons, no faculty-authored slide deck is bundled in this public-repository package. Add material locally through the app's upload control instead. The `data/faculty_materials/` folder is ignored by Git (except its placeholder file), so local course materials won't be added accidentally.

## Project layout

```text
Python_Learning_Chatbot/
├── app.py                       # Streamlit UI, lesson and quiz workflows
├── material_reader.py           # PDF/PPTX/DOCX/TXT extraction and retrieval
├── read_material.py             # Optional local PPTX inspection script
├── requirements.txt             # Python dependencies
├── README.md
├── GITHUB_UPLOAD_GUIDE.md        # Steps to publish the source to GitHub
├── .gitignore
├── data/
│   └── faculty_materials/
│       └── .gitkeep            # Keep the empty folder in Git
├── scripts/
│   ├── test_chunks.py           # Manual chunking demonstration
│   ├── test_material_reader.py  # Manual PPTX extraction demonstration
│   └── test_retrieval.py        # Manual retrieval demonstration
└── tests/
    └── test_text_processing.py # Automated unit tests
```

## Test the text-processing helpers

```bash
python -m unittest discover -s tests -v
```

To run the original demonstration scripts, for example:

```bash
python scripts/test_chunks.py
```

## Common problems

**Ollama connection error:** Check that Ollama is running and that `ollama pull llama3.2` completed successfully.

**`ModuleNotFoundError`:** Make sure you've activated the virtual environment and installed `requirements.txt`.

**Slow AI responses:** The model runs on your hardware. CPU inference can be noticeably slower, especially without a suitable GPU.

**Uploaded material seems ignored:** The document may not have extractable text, or its wording may not overlap sufficiently with your topic. Retrieval is keyword-based and only passes the top matching chunks to the model.

**GitHub Pages shows no app:** GitHub hosts the source code but cannot run this Python/Ollama app. Deploying it online requires a Streamlit-compatible server and an accessible Ollama backend, with appropriate security and resource configuration.

## Project status

This is an educational project. AI-generated examples and answer keys should be checked for correctness. The quiz parser expects a structured answer key from the model; malformed answers may require regenerating a quiz. This repository has been checked using static compilation and unit tests, but end-to-end model inference requires a running local Ollama installation.

## Licensing

No open-source license is included. If you plan to allow others to reuse or redistribute the code, choose an appropriate license and confirm you have the rights to license all included code and materials.
