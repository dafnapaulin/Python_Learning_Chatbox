from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from material_reader import retrieve_relevant_chunks

sample_text = """
Python has several data types.
Integers store whole numbers.
Floats store decimal numbers.
Strings store text.
Operators perform operations on values.
"""

question = "What is a string in Python?"

result = retrieve_relevant_chunks(sample_text, question)

print("Question:", question)
print("\nRelevant information:")
print(result)
