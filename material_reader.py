
from pptx import Presentation
from pypdf import PdfReader
from docx import Document
import os


def extract_text(file_path):
    """Extract text from a supported faculty material."""

    extension = os.path.splitext(file_path)[1].lower()
    extracted_text = []

    # Read PowerPoint files
    if extension == ".pptx":
        presentation = Presentation(file_path)

        for slide_number, slide in enumerate(
            presentation.slides, start=1
        ):
            slide_text = []

            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_text.append(shape.text.strip())

            if slide_text:
                extracted_text.append(
                    f"Slide {slide_number}\n"
                    + "\n".join(slide_text)
                )

    # Read PDF files
    elif extension == ".pdf":
        pdf = PdfReader(file_path)

        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()

            if text:
                extracted_text.append(
                    f"Page {page_number}\n{text.strip()}"
                )

    # Read Word documents
    elif extension == ".docx":
        document = Document(file_path)

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                extracted_text.append(paragraph.text.strip())

        # Also read tables in Word documents
        for table in document.tables:
            for row in table.rows:
                row_text = [
                    cell.text.strip() for cell in row.cells
                ]

                if any(row_text):
                    extracted_text.append(" | ".join(row_text))

    # Read text files
    elif extension == ".txt":
        with open(
            file_path, "r", encoding="utf-8-sig"
        ) as file:
            extracted_text.append(file.read())

    else:
        raise ValueError("Unsupported file type.")

    return "\n\n".join(extracted_text)


def split_into_chunks(text, chunk_size=180, overlap=40):
    """Split text into overlapping word-based chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        if end == len(words):
            break

        start = end - overlap

    return chunks


import re


def retrieve_relevant_chunks(text, query, top_k=3):
    """Find the text chunks most relevant to a question."""

    chunks = split_into_chunks(text)

    # Convert the question into lowercase keywords
    query_words = set(re.findall(r"\b[a-zA-Z0-9_]+\b", query.lower()))

    # Ignore common words that do not help much with searching
    stop_words = {
        "the", "is", "a", "an", "in", "on", "of", "to",
        "for", "and", "or", "what", "how", "why", "explain",
        "me", "give", "with", "are", "does", "do", "can"
    }

    query_words -= stop_words

    if not query_words:
        return ""

    # Calculate how many question keywords appear in each chunk
    scored_chunks = []

    for chunk in chunks:
        chunk_words = set(
            re.findall(r"\b[a-zA-Z0-9_]+\b", chunk.lower())
        )

        score = len(query_words & chunk_words)

        if score > 0:
            scored_chunks.append((score, chunk))

    # Put the most relevant chunks first
    scored_chunks.sort(key=lambda item: item[0], reverse=True)

    # Return the best matching chunks
    results = [
        chunk for score, chunk in scored_chunks[:top_k]
    ]

    return "\n\n".join(results)
