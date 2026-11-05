"""Automated, offline checks for text extraction and keyword retrieval."""
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from material_reader import extract_text, retrieve_relevant_chunks, split_into_chunks


class MaterialReaderTests(unittest.TestCase):
    def test_extract_text_from_txt(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "notes.txt"
            path.write_text("Python strings store text.", encoding="utf-8")
            self.assertEqual(extract_text(str(path)), "Python strings store text.")

    def test_extract_text_from_docx(self):
        from docx import Document

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "notes.docx"
            document = Document()
            document.add_paragraph("Python supports functions.")
            document.save(path)
            self.assertIn("Python supports functions.", extract_text(str(path)))

    def test_extract_text_from_pptx(self):
        from pptx import Presentation

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "notes.pptx"
            presentation = Presentation()
            slide = presentation.slides.add_slide(presentation.slide_layouts[5])
            slide.shapes.title.text = "Python data types"
            presentation.save(path)
            self.assertIn("Python data types", extract_text(str(path)))

    def test_empty_text_has_no_chunks(self):
        self.assertEqual(split_into_chunks(""), [])

    def test_overlap_keeps_context(self):
        self.assertEqual(
            split_into_chunks("one two three four five", chunk_size=3, overlap=1),
            ["one two three", "three four five"],
        )

    def test_invalid_chunk_parameters(self):
        with self.assertRaises(ValueError):
            split_into_chunks("abc", chunk_size=0)
        with self.assertRaises(ValueError):
            split_into_chunks("abc", chunk_size=3, overlap=3)

    def test_retrieval_matches_topic(self):
        text = (
            "Python strings store text. " * 30
            + "Python lists contain multiple values. " * 30
        )
        result = retrieve_relevant_chunks(text, "How do Python lists work?", top_k=1)
        self.assertIn("lists", result.lower())

    def test_retrieval_returns_empty_for_unrelated_question(self):
        self.assertEqual(retrieve_relevant_chunks("Python strings store text.", "elephants"), "")


if __name__ == "__main__":
    unittest.main()
