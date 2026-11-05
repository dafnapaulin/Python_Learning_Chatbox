from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from material_reader import split_into_chunks

sample_text = """
Python has several data types.
Integers store whole numbers.
Floats store decimal numbers.
Strings store text.
Operators perform operations on values.
"""

chunks = split_into_chunks(sample_text, chunk_size=10, overlap=3)

for number, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {number}:")
    print(chunk)

print("\nTotal chunks:", len(chunks))

