from pptx import Presentation
import glob
import os
from pathlib import Path

# Find all PowerPoint files in the local faculty materials folder.
material_directory = Path(__file__).resolve().parent / "data" / "faculty_materials"
pptx_files = glob.glob(str(material_directory / "*.pptx"))

if not pptx_files:
    print("No PPTX file found.")
else:
    print("Found PPTX file(s):")
    
    for file_path in pptx_files:
        print("\nFile:", os.path.basename(file_path))

        presentation = Presentation(file_path)

        print("Number of slides:", len(presentation.slides))

        for slide_number, slide in enumerate(presentation.slides, start=1):

            print(f"\n--- Slide {slide_number} ---")

            for shape in slide.shapes:

                if hasattr(shape, "text"):
                    text = shape.text.strip()

                    if text:
                        print(text)