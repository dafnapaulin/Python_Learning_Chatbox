import streamlit as st
import ollama
import hashlib
import tempfile
import os
import re
from material_reader import extract_text, retrieve_relevant_chunks

def generate_quiz(topic, faculty_context):
    quiz_prompt = f"""
Create exactly 5 multiple-choice questions about: {topic}

Use the following faculty material when relevant:
{faculty_context[:12000] if faculty_context else "No faculty material uploaded."}

IMPORTANT OUTPUT FORMAT:

1. Write each question on a new line.
2. Write options A, B, C, and D on four separate lines.
3. Never put two options on the same line.
4. Leave one blank line between questions.
5. Follow this exact structure:

1. Question text here
A. First option
B. Second option
C. Third option
D. Fourth option

Repeat this structure for questions 2, 3, 4, and 5.

After question 5 and all its options, write one final line:
ANSWER_KEY: 1=A, 2=B, 3=C, 4=D, 5=A

Replace the example answer letters with the actual correct answers.
The final line must begin exactly with ANSWER_KEY:
Do not add explanations or any text after the answer key.
"""
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "You are a friendly and accurate Python tutor."
            },
            {
                "role": "user",
                "content": quiz_prompt
            }
        ]
    )

    return response["message"]["content"]


# Page setup
st.set_page_config(
    page_title="Python Learning Chatbot",
    page_icon="🐍",
    layout="wide"
)

st.title("🐍 Python Learning Chatbot")
st.write("Learn Python step by step with your AI tutor.")


# Python concepts

python_topics = {
    "1. Python Fundamentals": [
        "Introduction to Python",
        "Features of Python",
        "Installing Python",
        "Python IDEs",
        "Writing the First Python Program",
        "Python Syntax and Indentation",
        "Comments",
        "Keywords and Identifiers",
        "Statements and Expressions",
        "Python Program Execution"
    ],

    "2. Variables and Constants": [
        "Variables",
        "Variable Naming Rules",
        "Assigning Values",
        "Multiple Assignment",
        "Constants",
        "Dynamic Typing",
        "Local and Global Variables",
        "Variable Scope"
    ],

    "3. Data Types and Operators": [
        "Introduction to Data Types",
        "Numeric Data Types",
        "Integer (int)",
        "Float (float)",
        "Complex Numbers",
        "Boolean (bool)",
        "String (str)",
        "List",
        "Tuple",
        "Set",
        "Dictionary",
        "Range",
        "None Type",
        "Mutable and Immutable Types",
        "Checking Data Types with type()",
        "Type Conversion",
        "Implicit Type Conversion",
        "Explicit Type Conversion",
        "Arithmetic Operators",
        "Addition, Subtraction, Multiplication and Division",
        "Floor Division (//)",
        "Modulus (%)",
        "Exponentiation (**)",
        "Comparison Operators",
        "Logical Operators",
        "Assignment Operators",
        "Compound Assignment Operators",
        "Bitwise Operators",
        "Membership Operators",
        "Identity Operators",
        "Operator Precedence",
        "Operator Associativity",
        "Expressions and Evaluation"
    ],

    "4. Input and Output": [
        "print() Function",
        "input() Function",
        "Displaying Multiple Values",
        "Separators and End Parameters",
        "Formatted Output",
        "f-Strings",
        "format() Method",
        "Escape Characters"
    ],

    "5. Conditional Statements": [
        "Decision Making",
        "if Statement",
        "if-else Statement",
        "if-elif-else Statement",
        "Nested if Statements",
        "Conditional Expressions",
        "Pass Statement"
    ],

    "6. Loops and Iteration": [
        "Introduction to Loops",
        "while Loop",
        "for Loop",
        "range() Function",
        "Nested Loops",
        "break Statement",
        "continue Statement",
        "Loop else Clause",
        "Infinite Loops",
        "Iterables and Iterators"
    ],

    "7. Strings": [
        "Creating Strings",
        "String Indexing",
        "String Slicing",
        "String Immutability",
        "String Operators",
        "String Methods",
        "Searching in Strings",
        "Replacing Strings",
        "Splitting and Joining Strings",
        "String Formatting",
        "String Comparison",
        "Common String Programs"
    ],

    "8. Lists": [
        "Creating Lists",
        "Accessing List Elements",
        "List Indexing and Slicing",
        "Updating Lists",
        "Adding Elements",
        "Removing Elements",
        "List Methods",
        "List Traversal",
        "Nested Lists",
        "List Comprehensions",
        "Copying Lists",
        "Common List Programs"
    ],

    "9. Tuples": [
        "Creating Tuples",
        "Accessing Tuple Elements",
        "Tuple Indexing and Slicing",
        "Tuple Packing and Unpacking",
        "Tuple Methods",
        "Nested Tuples",
        "Lists vs Tuples"
    ],

    "10. Sets": [
        "Creating Sets",
        "Adding and Removing Elements",
        "Set Methods",
        "Union",
        "Intersection",
        "Difference",
        "Symmetric Difference",
        "Subset and Superset",
        "Frozen Sets",
        "Sets vs Lists"
    ],

    "11. Dictionaries": [
        "Creating Dictionaries",
        "Accessing Values",
        "Adding and Updating Items",
        "Removing Items",
        "Dictionary Methods",
        "Keys and Values",
        "Traversing Dictionaries",
        "Nested Dictionaries",
        "Dictionary Comprehensions",
        "Common Dictionary Programs"
    ],

    "12. Functions": [
        "Introduction to Functions",
        "Defining Functions",
        "Calling Functions",
        "Parameters and Arguments",
        "Positional Arguments",
        "Keyword Arguments",
        "Default Parameters",
        "Variable-Length Arguments (*args)",
        "Keyword Variable Arguments (**kwargs)",
        "return Statement",
        "Multiple Return Values",
        "Local and Global Scope",
        "Lambda Functions",
        "Recursive Functions",
        "Docstrings",
        "Function Annotations"
    ],

    "13. Modules and Packages": [
        "Introduction to Modules",
        "import Statement",
        "from-import Statement",
        "Aliases with as",
        "Built-in Modules",
        "math Module",
        "random Module",
        "datetime Module",
        "os Module",
        "Creating Custom Modules",
        "Python Packages",
        "pip and Installing Packages"
    ],

    "14. Comprehensions and Functional Tools": [
        "List Comprehensions",
        "Set Comprehensions",
        "Dictionary Comprehensions",
        "Generator Expressions",
        "map() Function",
        "filter() Function",
        "zip() Function",
        "enumerate() Function",
        "any() and all()"
    ],

    "15. Exception Handling": [
        "Errors and Exceptions",
        "Syntax Errors",
        "Runtime Errors",
        "try and except",
        "Handling Multiple Exceptions",
        "else Clause",
        "finally Clause",
        "raise Statement",
        "Custom Exceptions",
        "Assertions"
    ],

    "16. File Handling": [
        "Opening Files",
        "File Modes",
        "Reading Files",
        "Writing Files",
        "Appending to Files",
        "Closing Files",
        "with Statement",
        "File Pointer and seek()",
        "Working with Text Files",
        "Working with CSV Files",
        "Working with JSON Files",
        "File and Directory Operations"
    ],

    "17. Object-Oriented Programming": [
        "Introduction to OOP",
        "Classes and Objects",
        "Attributes and Methods",
        "The __init__() Method",
        "self Parameter",
        "Instance Variables",
        "Class Variables",
        "Instance Methods",
        "Class Methods",
        "Static Methods",
        "Encapsulation",
        "Inheritance",
        "Multiple Inheritance",
        "Polymorphism",
        "Method Overriding",
        "Abstraction",
        "Properties",
        "Special Methods",
        "Composition"
    ],

    "18. Iterators and Generators": [
        "Iterable Objects",
        "Iterator Protocol",
        "iter() and next()",
        "Creating Custom Iterators",
        "Generators",
        "yield Keyword",
        "Generator Expressions",
        "Generator vs Iterator"
    ],

    "19. Advanced Python Concepts": [
        "Decorators",
        "Closures",
        "Higher-Order Functions",
        "Context Managers",
        "with Statement",
        "Type Hints",
        "Annotations",
        "Dataclasses",
        "Shallow Copy and Deep Copy",
        "Memory Management Basics"
    ],

    "20. Regular Expressions": [
        "Introduction to Regular Expressions",
        "re Module",
        "Matching Patterns",
        "Searching Text",
        "Character Classes",
        "Quantifiers",
        "Groups",
        "Substitution",
        "Validating Text"
    ],

    "21. Data Structures and Algorithms": [
        "Algorithm Basics",
        "Time and Space Complexity",
        "Arrays and Lists",
        "Stacks",
        "Queues",
        "Linked Lists",
        "Hash Tables",
        "Linear Search",
        "Binary Search",
        "Bubble Sort",
        "Selection Sort",
        "Insertion Sort",
        "Merge Sort",
        "Quick Sort",
        "Recursion and Backtracking",
        "Basic Tree Concepts",
        "Basic Graph Concepts"
    ],

    "22. Useful Python Libraries": [
        "Introduction to Libraries",
        "NumPy Basics",
        "Pandas Basics",
        "Matplotlib Basics",
        "Requests Basics",
        "Working with Dates",
        "JSON Processing",
        "CSV Processing"
    ],

    "23. Database Programming": [
        "Database Basics",
        "SQL Basics",
        "SQLite with Python",
        "Connecting to a Database",
        "Executing Queries",
        "Insert, Update and Delete",
        "Fetching Records",
        "Parameterized Queries"
    ],

    "24. Testing and Debugging": [
        "Reading Error Messages",
        "Debugging Basics",
        "Using print() for Debugging",
        "VS Code Debugger",
        "Assertions",
        "Unit Testing",
        "unittest Module",
        "pytest Basics",
        "Test Cases"
    ],

    "25. Python Projects and Practice": [
        "Basic Calculator",
        "Number Guessing Game",
        "Multiplication Table Generator",
        "Student Marks Calculator",
        "To-Do List",
        "Password Generator",
        "Contact Book",
        "File Organizer",
        "Quiz Application",
        "Mini Data Analysis Project"
    ]
}


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "faculty_text" not in st.session_state:
    st.session_state.faculty_text = ""

if "faculty_hash" not in st.session_state:
    st.session_state.faculty_hash = ""

if "uploaded_name" not in st.session_state:
    st.session_state.uploaded_name = ""

if "lesson_topic" not in st.session_state:
    st.session_state.lesson_topic = ""

if "lesson_content" not in st.session_state:
    st.session_state.lesson_content = ""

if "show_topic_picker" not in st.session_state:
    st.session_state.show_topic_picker = False

if "auto_lesson" not in st.session_state:
    st.session_state.auto_lesson = False

if "lesson_cache_key" not in st.session_state:
    st.session_state.lesson_cache_key = ""

if "upload_nonce" not in st.session_state:
    st.session_state.upload_nonce = 0

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = ""

if "quiz_answer_key" not in st.session_state:
    st.session_state.quiz_answer_key = {}

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None
   

st.sidebar.header("Learning Settings")
st.sidebar.subheader("📚 Learn Python")

if st.sidebar.button("Choose Topic"):
    st.session_state.show_topic_picker = True

if st.session_state.show_topic_picker:

    selected_category = st.sidebar.selectbox(
        "Choose a main topic:",
        list(python_topics.keys()),
        key="main_topic_select"
    )

    selected_concept = st.sidebar.selectbox(
        "Choose a subtopic:",
        python_topics[selected_category],
        key="subtopic_select"
    )

    st.session_state.auto_lesson = st.sidebar.toggle(
        "Automatically show lesson",
        value=st.session_state.auto_lesson,
        help=(
            "Turn this on to generate a lesson "
            "when you choose a subtopic. Turn it off "
            "to learn through chat instead."
        )
    )

else:
    selected_category = list(python_topics.keys())[0]
    selected_concept = python_topics[selected_category][0]

    st.sidebar.caption(
        "Click 'Choose Topic' to browse Python lessons."
    )


st.sidebar.info(
    f"Main topic: {selected_category}\n\n"
    f"Selected subtopic: {selected_concept}"
)

st.sidebar.subheader("Faculty Study Material")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF, PPTX, DOCX or TXT",
    type=["pdf", "pptx", "docx", "txt"],
    key=f"faculty_upload_{st.session_state.upload_nonce}",
)


if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    current_hash = hashlib.sha256(file_bytes).hexdigest()

    if current_hash != st.session_state.faculty_hash:
        temp_path = None

        try:
            suffix = os.path.splitext(uploaded_file.name)[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:
                temp_file.write(file_bytes)
                temp_path = temp_file.name

            extracted_text = extract_text(temp_path)

            st.session_state.faculty_text = extracted_text
            st.session_state.faculty_hash = current_hash
            st.session_state.uploaded_name = uploaded_file.name

            st.sidebar.success("Study material loaded!")

        except Exception as error:
            st.sidebar.error(f"Could not read file: {error}")

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)


if st.session_state.uploaded_name:
    st.sidebar.write(
        f"Loaded file: {st.session_state.uploaded_name}"
    )

    if st.sidebar.button("Remove study material"):
        st.session_state.faculty_text = ""
        st.session_state.faculty_hash = ""
        st.session_state.uploaded_name = ""
        st.session_state.upload_nonce += 1
        st.rerun()

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()


st.subheader("How would you like to learn?")

learning_mode = st.selectbox(
    "Choose a learning mode:",
    [
        "Explain Concept",
        "Explain Simply",
        "Show Python Code",
        "Give an Example",
        "Practice",
        "Quiz"
    ]
)


# Generate a lesson only when the student chooses automatic mode
if st.session_state.show_topic_picker:

    current_topic = f"{selected_category} - {selected_concept}"
    current_lesson_key = (
        f"{current_topic}|{learning_mode}|{st.session_state.faculty_hash}"
    )

    if (
        st.session_state.auto_lesson
        and learning_mode == "Quiz"
        and current_lesson_key != st.session_state.lesson_cache_key
    ):

        with st.spinner("Preparing your quiz..."):
            try:
                faculty_context = retrieve_relevant_chunks(
                    st.session_state.faculty_text,
                    f"{selected_category} {selected_concept}",
                    top_k=3
                )

                answer = generate_quiz(
                    current_topic,
                    faculty_context
                )

                if "ANSWER_KEY:" not in answer:
                    st.warning(
                        "The quiz answer key was not generated. "
                        "Please try again."
                    )
                else:
                    quiz_text, key_text = answer.split(
                        "ANSWER_KEY:", 1
                    )

                    matches = re.findall(
                        r"([1-5])\s*=\s*([A-D])",
                        key_text.upper()
                    )
                    if (
                        len(matches) == 5
                        and {q for q, _ in matches} == set("12345")
                    ):
                        st.session_state.quiz_answer_key = {
                            int(q): option
                            for q, option in matches
                        }
                        st.session_state.quiz_questions = quiz_text.strip()
                        st.session_state.quiz_active = True
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_score = None

                        st.session_state.lesson_content = quiz_text.strip()
                        st.session_state.lesson_topic = current_topic
                        st.session_state.lesson_cache_key = current_lesson_key

                        st.success("Your quiz is ready!")
                        
                    else:
                        st.warning(
                            "The quiz answer key is invalid. "
                            "Please try again."
                        )

            except Exception as error:
                st.error(f"Could not generate quiz: {error}")
    if st.session_state.auto_lesson and learning_mode != "Quiz":

        if current_lesson_key != st.session_state.lesson_cache_key:

            with st.spinner("Preparing your lesson..."):
                try:
                    
                    faculty_context = retrieve_relevant_chunks(
                    st.session_state.faculty_text,
                    f"{selected_category} {selected_concept}",
                    top_k=3
)
                    lesson_prompt = f"""
You are a friendly Python programming teacher.

Main topic: {selected_category}
Subtopic: {selected_concept}

Teach this topic using proper Markdown formatting.

1. ## Definition
2. ## Simple Explanation
3. ## Important Points
   - Use bullet points.
4. ## Python Code Examples
   - Put every Python example inside a fenced code block using ```python.
5. ## Expected Output
   - Put program output inside fenced code blocks.
6. ## Step-by-Step Explanation
   - Use a numbered list.
7. ## Common Mistakes
   - Use bullet points.
8. ## Short Summary
9. ## Practice Questions
   - Give exactly three questions.

IMPORTANT FORMATTING RULES:
- Use Markdown headings starting with ##.
- Use **bold** only for important words.
- Use proper bullet points and numbered lists.
- Put all Python code inside ```python and ``` fences.
- Never write code without code fences.
- Do not use lines of ==== or ---- as headings.
- Return only the lesson content, without extra introductions.
Use simple English.

Markdown formatting requirements:
- Use Markdown headings for each section.
- Put every complete Python code example in a separate fenced code block, starting with ```python and ending with ```.
- Never put a complete code example inside inline backticks.
- Put each example's expected output in a separate fenced code block.
- Keep code, comments, and output on separate, readable lines.

Code accuracy and formatting rules:
- Verify that all Python code examples are syntactically correct and use concepts appropriately.
- Ensure that every example follows Python's rules and avoids invalid operations.
- Display each complete code example in a properly formatted Python code block.
- Show the expected output separately and ensure it matches the code.
- Keep comments and indentation correctly formatted inside code blocks.
- Explain code examples step by step using simple English.
- Identify common mistakes relevant to the selected topic and explain how to avoid them.
- Adapt all explanations, examples, and practice questions to the selected topic and the student's learning level.
- If an operation or concept has limitations, explain them accurately.

If faculty material is available, use it as the
primary source. If it does not cover the topic,
clearly distinguish your general Python explanation.

Faculty material:
{faculty_context[:12000] if faculty_context else "No faculty material uploaded."}
"""

                    response = ollama.chat(
                        model="llama3.2",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a friendly Python tutor."
                                )
                            },
                            {
                                "role": "user",
                                "content": lesson_prompt
                            }
                        ]
                    )

                    st.session_state.lesson_content = (
                        response["message"]["content"]
                    )
                    st.session_state.lesson_topic = current_topic
                    st.session_state.lesson_cache_key = current_lesson_key

                except Exception as error:
                    st.error(f"Could not generate lesson: {error}")

    # Display only the lesson belonging to the selected topic
    if (
        st.session_state.auto_lesson
        and st.session_state.lesson_cache_key == current_lesson_key
        and st.session_state.lesson_content
    ):
        
        st.divider()
        st.header(f"📘 {selected_concept}")
        st.caption(f"Main topic: {selected_category}")

        with st.container():
            st.markdown(st.session_state.lesson_content)
    elif not st.session_state.auto_lesson:
        st.info(
            "Automatic lessons are off. You can ask questions "
            "using the chat box whenever you are ready."
        )

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_question = st.chat_input(
    "Ask a question about Python..."
)

if user_question:
    question_lower = user_question.lower().strip()

    # Handle requests about the current quiz first
    if (
    st.session_state.quiz_active
    and st.session_state.quiz_answer_key
):

        if any(phrase in question_lower for phrase in [
            "give me the answers",
            "show the answers",
            "answer key",
            "tell me the answers",
            "what are the answers"
        ]):
            answer_text = "\n".join(
                f"Question {q}: {answer}"
                for q, answer in sorted(
                    st.session_state.quiz_answer_key.items()
                )
            )

            st.session_state.messages.append({
                "role": "user",
                "content": user_question
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    "Here are the answers to your current quiz:\n\n"
                    + answer_text
                )
            })

            st.rerun()

    if (
        learning_mode == "Quiz"
        and st.session_state.quiz_active
        and not st.session_state.quiz_submitted
        and st.session_state.quiz_answer_key
        and  re.search(
                r"\b1\s*[.)=:-]\s*[A-D]\b",
                user_question.upper()
        )
    ):
        submitted_answers = dict(
            (int(q), a)
            for q, a in re.findall(
                r"\b([1-5])\s*[.)=:-]\s*([A-D])\b",
                user_question.upper()
            )
        )

        if len(submitted_answers) == 5:
            score = sum(
                submitted_answers.get(q) == correct
                for q, correct in st.session_state.quiz_answer_key.items()
            )

            st.session_state.quiz_score = score
            st.session_state.quiz_submitted = True

            st.session_state.messages.append({
                "role": "user",
                "content": user_question
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    f"Your score: {score}/5\n\n"
                    + "\n".join(
                        f"Question {q}: "
                        f"Your answer: {submitted_answers.get(q, 'Not answered')} | "
                        f"Correct answer: {correct} | "
                        f"{'Correct ✅' if submitted_answers.get(q) == correct else 'Incorrect ❌'}"
                        for q, correct in sorted(
                             st.session_state.quiz_answer_key.items()
                        )
                    )
                )
            })
            st.rerun()
        st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    mode_instructions = {
        "Explain Concept": (
            "Explain the concept clearly with important points."
        ),
        "Explain Simply": (
            "Explain in very simple English, like teaching a beginner."
        ),
        "Show Python Code": (
            "Give a short, correct Python program and explain it line by line."
        ),
        "Give an Example": (
            "Give a practical example with code and its output."
        ),
        "Practice": (
            "Generate exactly ONE Python practice question at a time "
            "based on the selected concept. Do not generate multiple "
            "questions in one response. Show the question and, when "
            "relevant, a code template with a placeholder. Do not reveal "
            "the solution immediately. Wait for the student's attempt. "
            "When the student submits an answer, evaluate that attempt "
            "before moving to another question. Do not automatically "
            "generate another question after giving feedback."
        ),
           
        "Quiz": (
            "Create exactly 5 multiple-choice questions about the selected "
            "Python concept. Number them 1 to 5. Each question must have "
            "exactly four options, A, B, C, and D. Put every option on its "
            "own separate line. Use this format:\n\n"
            "Question 1: [question text]\n"
            "A. [first option]\n"
            "B. [second option]\n"
            "C. [third option]\n"
            "D. [fourth option]\n\n"
            "Repeat this format for all five questions. Do not print standalone "
            "A, B, C, or D lines. Do not repeat the quiz. Do not add a lesson "
            "heading or lesson explanation. Each question must have exactly "
            "one correct answer.\n"
            "After the questions, add one final line in this exact format: "
            "ANSWER_KEY: 1=A, 2=B, 3=C, 4=D, 5=A. Replace these example "
            "letters with the actual answers. Do not put the answer key "
            "inside the student-facing quiz."
        ),


         
    }

    
    faculty_text = st.session_state.faculty_text

    faculty_context = retrieve_relevant_chunks(
            faculty_text,
            f"{selected_category} {selected_concept} {user_question}",
            top_k=3
        )

    if not faculty_context:
            faculty_context = (
                "No relevant information found in the "
                "uploaded faculty material."
            )


    prompt = f"""
You are a friendly Python programming teacher.

Main topic: {selected_category}
Selected subtopic: {selected_concept}
Learning mode: {learning_mode}

Student's question:
{user_question}

Instructions:
{mode_instructions[learning_mode]}

Rules:
- Follow the instructions for the selected learning mode.
- Do not use the Explain Concept structure for every mode.
- Use only the headings and formatting needed for the selected mode.
- Use simple English suitable for a Python beginner.
- Keep answers focused on the student's request.
- Use correct Python syntax whenever providing code.
- Include code output only when relevant to the selected mode.
- Use faculty material as the primary source when relevant.
- If no faculty material is available, use accurate general Python knowledge.
- Do not invent information or claim that content came from faculty material when it did not.
- In Quiz mode, follow the exact quiz format and provide the answer key for internal grading.

Faculty study material:
{faculty_context[:12000] if faculty_context else "No faculty material uploaded."}

Keep the response focused on Python programming.
"""
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = ollama.chat(
                    model="llama3.2",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a friendly and accurate "
                                "Python programming tutor."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                answer = response["message"]["content"]

                if learning_mode == "Quiz":
                    if "ANSWER_KEY:" in answer:
                        quiz_text, key_text = answer.split("ANSWER_KEY:", 1)

                        matches = re.findall(
                           r"\b([1-5])\s*=\s*([A-D])\b",
                           key_text.upper()
                        )

                        if len(matches) == 5 and len({q for q, _ in matches}) == 5:
                           st.session_state.quiz_answer_key = {
                              int(question): option
                              for question, option in matches
                           }
                           st.session_state.quiz_questions = quiz_text
                           st.session_state.quiz_active = True
                           st.session_state.quiz_submitted = False
                           st.session_state.quiz_score = None
                           st.markdown(quiz_text.strip().replace("\n", "  \n"))

                        else:
                           st.warning("The quiz answer key is invalid. Please generate the quiz again.")
                    else:
                           st.warning("No answer key was generated. Please generate the quiz again.")

                else:
                    st.markdown(answer)

                # Never expose an answer key in the conversation history.
                if learning_mode == "Quiz":
                    if (
                        "ANSWER_KEY:" in answer
                        and len(matches) == 5
                        and len({q for q, _ in matches}) == 5
                    ):
                        visible_answer = quiz_text.strip()
                    else:
                        visible_answer = (
                            "Unable to generate a valid quiz. Please try again."
                        )
                else:
                    visible_answer = answer

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": visible_answer,
                })

            except Exception as error:
                st.error(
                    "Could not connect to Ollama. "
                    "Make sure Ollama is running and "
                    "the llama3.2 model is installed."
                )
                st.code(str(error))


