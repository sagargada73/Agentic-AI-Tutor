
# AI Tutor for Programming

AI Tutor is an interactive learning platform designed to teach programming concepts. It combines adaptive learning, interactive quizzes, progress tracking, and an AI-powered chatbot to create a personalized and engaging learning experience.

---

## **Features**

- **Lessons and Quizzes**:
  - Interactive lessons on Python basics.
  - Quizzes with automatic feedback to test your knowledge.

- **Adaptive Learning**:
  - Tracks your progress and suggests the next lesson dynamically.
  - Recommends lessons to review based on quiz performance.

- **Progress Tracking**:
  - Tracks your learning streak and completed lessons.
  - Earn badges based on achievements like maintaining streaks or scoring full marks in quizzes.

- **Real-Time Chatbot**:
  - AI-powered chatbot for answering programming-related questions.

---

## **Technologies Used**

- **Frontend**: [Streamlit](https://streamlit.io/) for a user-friendly web interface.
- **Backend**: Python for handling logic, tracking progress, and lesson management.
- **AI Model**: Hugging Face Transformers (`Salesforce/codegen-350M-mono`) for the chatbot.
- **Data Storage**: JSON files for storing user progress and quiz results.

---

## **File Structure**

```
AI-Tutor/
├── app.py                  # Main application file
├── lessons/                # Directory containing lesson JSON files
│   ├── intro_to_python.json
│   ├── variables_and_data_types.json
│   ├── conditionals.json
│   ├── loops.json
│   ├── functions.json
├── quizzes/                # Directory containing quiz JSON files
│   ├── intro_to_python_quiz.json
│   ├── variables_and_data_types_quiz.json
│   ├── conditionals_quiz.json
│   ├── loops_quiz.json
│   ├── functions_quiz.json
├── user_data/              # Directory for storing user progress data
│   └── progress.json       # Tracks user progress (created at runtime)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## **Future Scope**

The project can be expanded with the following features:
- **Advanced Lessons**:
  - Add more topics such as object-oriented programming, data structures, and algorithms.

- **Quiz Difficulty Levels**:
  - Include multiple levels of difficulty for quizzes (easy, medium, hard).

- **Gamification Features**:
  - Leaderboards to compare progress with other learners.
  - Additional badges for milestones like completing all quizzes or maintaining a 30-day streak.

- **Multi-Language Support**:
  - Support for teaching other programming languages (e.g., Java, C++, JavaScript).

- **User Accounts**:
  - Integrate a database for user accounts to save progress online.

---

## **License**

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software as long as proper attribution is provided.

---

## **Steps to Clone and Run the Project**

### **Prerequisites**
- Python 3.8 or later installed on your system.
- pip (Python package manager).

### **Steps to Run the Project**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sagargada73/Agentic-AI-Tutor.git
   ```
   Navigate to the project directory:
   ```bash
   cd AI-Tutor
   ```

2. **Install Dependencies**:
   Install the required Python libraries listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
   This will open the app in your default web browser.

4. **Start Learning**:
   - Explore lessons, take quizzes, and chat with the AI-powered chatbot.

---
