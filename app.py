import streamlit as st
import json
import os
from datetime import datetime, timedelta
import requests
import time

# Load and Save JSON Data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Initialize Progress File if Missing
progress_file = "user_data/progress.json"
if not os.path.exists(progress_file):
    initial_data = {
        "completed_lessons": [],
        "quiz_scores": {},
        "last_learning_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "streak_count": 1,
        "badges": [],
        "learning_goal": {}
    }
    os.makedirs(os.path.dirname(progress_file), exist_ok=True)  # Create user_data directory if it doesn't exist
    save_json(initial_data, progress_file)
else:
    # If the file exists, load and check for missing keys
    progress = load_json(progress_file)
    if "badges" not in progress:
        progress["badges"] = []
    if "learning_goal" not in progress:
        progress["learning_goal"] = {}
    if "quiz_scores" not in progress:
        progress["quiz_scores"] = {}
    save_json(progress, progress_file)

# Load Progress
progress = load_json(progress_file)

# Streak System
def update_streak():
    try:
        # Try parsing with timestamp format
        last_learning_time = datetime.strptime(progress["last_learning_time"], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        # Fallback to date-only format
        last_learning_time = datetime.strptime(progress["last_learning_time"], "%Y-%m-%d")
    
    today = datetime.now().date()
    if last_learning_time.date() == today:
        return  # Already interacted today

    # Check if yesterday was the last learning day
    if (today - last_learning_time.date()).days == 1:
        progress["streak_count"] += 1
    else:
        progress["streak_count"] = 1  # Reset streak

    # Update last learning time
    progress["last_learning_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_json(progress, progress_file)

# Badge System
def check_badges():
    # Ensure the 'badges' key exists
    if "badges" not in progress:
        progress["badges"] = []

    badges = progress["badges"]

    # Badge: Complete all lessons
    if len(progress["completed_lessons"]) == len(lessons) and "Lesson Master" not in badges:
        badges.append("Lesson Master")

    # Badge: Score 100% on a quiz
    for score in progress["quiz_scores"].values():
        if score == 100 and "Quiz Champ" not in badges:
            badges.append("Quiz Champ")
            break

    # Badge: Maintain a streak of 7 days
    if progress["streak_count"] >= 7 and "Streak Star" not in badges:
        badges.append("Streak Star")

    progress["badges"] = badges
    save_json(progress, progress_file)

# Initialize API key in session state if not present
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

# Ollama Integration
def get_ollama_response(question, api_key=None):
    headers = {'Content-Type': 'application/json'}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    
    prompt = (
        "You are a Python programming tutor. Answer the following question with examples:\n\n"
        f"{question}"
    )
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'codellama',
                    'prompt': prompt,
                    'stream': False
                },
                headers=headers,
                timeout=30  # Add timeout
            )
            if response.status_code == 200:
                return response.json()['response']
            else:
                retry_count += 1
                if retry_count == max_retries:
                    return f"Error: Failed to get response from Ollama. Status code: {response.status_code}"
                st.warning(f"Retrying... Attempt {retry_count} of {max_retries}")
                time.sleep(1)  # Wait 1 second before retrying
        except requests.exceptions.ConnectionError:
            retry_count += 1
            if retry_count == max_retries:
                return "Error: Could not connect to Ollama. Please ensure Ollama is running (check if 'ollama serve' is running in terminal)"
            st.warning(f"Connection failed. Retrying... Attempt {retry_count} of {max_retries}")
            time.sleep(1)
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

# Clean Response Function
def clean_response(response):
    lines = response.split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line and line not in cleaned_lines:
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

# Get Hugging Face Response
def get_hf_response(question):
    prompt = (
        "You are a Python programming assistant. Provide accurate answers to questions about Python and include examples. "
        "For example:\n\n"
        "Q: How do I add two variables in Python?\n"
        "A: To add two variables in Python, you can use the + operator. For example:\n"
        "```python\n"
        "a = 5\n"
        "b = 10\n"
        "c = a + b\n"
        "print(c)  # Output: 15\n"
        "```\n\n"
        f"Q: {question}\n"
        "A:"
    )
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            max_length=250,
            num_return_sequences=1,
            repetition_penalty=1.2,
            temperature=0.7,
        )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return clean_response(response.split("A:")[-1].strip())

# Check User Answers
def check_answers(questions, user_answers):
    score = 0
    for i, question in enumerate(questions):
        if user_answers[i] == question["answer"]:
            score += 1
    return score

# Lessons and Quizzes
lessons = [
    {"title": "Introduction to Python", "file": "lessons/intro_to_python.json"},
    {"title": "Variables and Data Types", "file": "lessons/variables_and_data_types.json"},
    {"title": "Conditionals in Python", "file": "lessons/conditionals.json"},
    {"title": "Loops in Python", "file": "lessons/loops.json"},
    {"title": "Functions in Python", "file": "lessons/functions.json"}
]

quizzes = [
    {"title": "Quiz: Introduction to Python", "file": "quizzes/intro_to_python_quiz.json"},
    {"title": "Quiz: Variables and Data Types", "file": "quizzes/variables_and_data_types_quiz.json"},
    {"title": "Quiz: Conditionals", "file": "quizzes/conditionals_quiz.json"},
    {"title": "Quiz: Loops", "file": "quizzes/loops_quiz.json"},
    {"title": "Quiz: Functions", "file": "quizzes/functions_quiz.json"}
]

# App Layout
st.title("AI Tutor for Programming")

# Update streak and badges
update_streak()
check_badges()

menu = st.sidebar.radio("Menu", ["Lesson", "Quiz", "Progress", "Set Learning Goal", "Chatbot"])

# Set Learning Goal
if menu == "Set Learning Goal":
    st.header("Set Your Learning Goal")
    
    goal_description = st.text_input("What is your learning goal?", "Complete Python basics in 2 weeks")
    duration = st.number_input("How many days do you want to complete it in?", min_value=1, max_value=30, value=14)
    
    if st.button("Set Goal"):
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration)
        lesson_plan = [lesson["title"] for lesson in lessons]
        
        progress["learning_goal"] = {
            "goal_description": goal_description,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "lesson_plan": lesson_plan,
            "completed_lessons": []
        }
        save_json(progress, progress_file)
        st.success(f"Goal set: {goal_description} by {end_date.strftime('%Y-%m-%d')}")

# Lessons Section
elif menu == "Lesson":
    selected_lesson = st.selectbox("Select a Lesson", [lesson["title"] for lesson in lessons])
    lesson_file = next(lesson["file"] for lesson in lessons if lesson["title"] == selected_lesson)
    lesson = load_json(lesson_file)
    
    st.header(lesson["title"])
    for paragraph in lesson["content"]:
        st.write(paragraph)

    if st.button("Mark as Completed"):
        if selected_lesson not in progress["completed_lessons"]:
            progress["completed_lessons"].append(selected_lesson)
            save_json(progress, progress_file)
            st.success(f"'{selected_lesson}' marked as completed!")

# Quizzes Section
elif menu == "Quiz":
    selected_quiz = st.selectbox("Select a Quiz", [quiz["title"] for quiz in quizzes])
    quiz_file = next(quiz["file"] for quiz in quizzes if quiz["title"] == selected_quiz)
    quiz = load_json(quiz_file)

    # Check if the corresponding lesson is completed
    required_lesson = selected_quiz.lower().replace("quiz: ", "").strip()
    if required_lesson in [lesson.lower() for lesson in progress["completed_lessons"]]:
        st.header(quiz["title"])
        user_answers = []
        for question in quiz["questions"]:
            st.write(question["question"])
            options = question["options"]
            user_answers.append(st.radio("Select an answer:", options, key=question["question"]))

        if st.button("Submit Quiz"):
            score = check_answers(quiz["questions"], user_answers)
            st.success(f"Your Score: {score}/{len(quiz['questions'])}")

            progress["quiz_scores"][selected_quiz.lower().replace(" ", "_")] = score
            save_json(progress, progress_file)

            if score == len(quiz["questions"]):
                st.write("Great job! You can move to a higher difficulty level.")
            elif score >= len(quiz["questions"]) // 2:
                st.write("Good work! Keep practicing to improve.")
            else:
                st.write("Don't worry! Review the lesson and try again.")
    else:
        st.warning("Complete the corresponding lesson first.")

# Progress Section
elif menu == "Progress":
    st.header("Your Learning Progress")
    
    if "learning_goal" in progress and progress["learning_goal"]:
        goal = progress["learning_goal"]
        st.write(f"**Goal**: {goal['goal_description']}")
        st.write(f"**Deadline**: {goal['end_date']}")
        remaining_lessons = [lesson for lesson in goal["lesson_plan"] if lesson not in progress["completed_lessons"]]
        st.write("**Remaining Lessons**:")
        for lesson in remaining_lessons:
            st.write(f"- {lesson}")

        days_left = (datetime.strptime(goal["end_date"], "%Y-%m-%d") - datetime.now()).days
        if days_left < len(remaining_lessons):
            st.warning(f"You are behind schedule! {len(remaining_lessons)} lessons remain, but only {days_left} days left.")
        else:
            st.success(f"You're on track! {len(remaining_lessons)} lessons left in {days_left} days.")
    else:
        st.write("No learning goal set yet.")
    
    # Show streak count
    st.write(f"### Current Learning Streak: {progress['streak_count']} days")
    
    # Show badges
    st.write("### Badges Earned")
    for badge in progress["badges"]:
        st.write(f"- {badge}")
    
    # Show quiz scores
    st.write("### Quiz Scores")
    for quiz, score in progress["quiz_scores"].items():
        st.write(f"{quiz}: {score} points")

# Chatbot Section
elif menu == "Chatbot":
    st.header("AI Chatbot for Real-Time Q&A")
    
    # Add API key input in sidebar
    with st.sidebar:
        api_key = st.text_input("Enter API Key (optional):", type="password")
        if api_key:
            st.session_state.api_key = api_key
    
    user_input = st.text_area("Ask your programming-related question here:")
    if st.button("Get Answer"):
        if user_input.strip():
            response = get_ollama_response(user_input, st.session_state.api_key)
            st.write("**AI Response:**")
            st.write(response)
        else:
            st.warning("Please enter a valid question!")