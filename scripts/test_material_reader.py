from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from material_reader import extract_text
import glob
import os

# Find a faculty PowerPoint file
files = glob.glob(str(Path(__file__).resolve().parents[1] / "data" / "faculty_materials" / "*.pptx"))

if files:
    file_path = files[0]

    print("Reading:", os.path.basename(file_path))

    text = extract_text(file_path)

    print("\nExtracted text:\n")
    print(text[:2000])

else:
    print("No PowerPoint file found!")