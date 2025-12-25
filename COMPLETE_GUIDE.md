# Complete Quiz Mode Setup & Operation Guide

## 🎯 Everything You Need to Know

---

## Part 1: Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser
- Terminal/Command Prompt

### Step 1: Navigate to Backend Directory
```bash
cd c:\Users\SAMINATHAN\OneDrive\Desktop\h25-lms\backend
```

### Step 2: Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# If venv doesn't exist, create it:
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Requirements (if needed)
```bash
pip install -r requirements.txt
```

### Step 4: Seed Database with Questions
```bash
python seed_questions.py
```

**Expected Output:**
```
✅ Added: What is the correct way to create a list in Python?...
✅ Added: What keyword is used to create a function in Python?...
✅ Added: Which of the following is a mutable data type in Python?...
✅ Added: What does CSRF stand for?...
✅ Added: What is the primary purpose of HTTPS?...
✅ Added: What is SQL Injection?...
✅ Added: Which layer of the OSI model is responsible for routing?...
✅ Added: What does TCP stand for?...
✅ Added: What is the default port for HTTP?...
✅ Added: What does chmod 755 mean in Linux?...
✅ Added: What is the purpose of sudo in Linux?...
✅ Added: Which file in Linux typically contains user account information?...
✅ Added: Which algorithm is most commonly used for symmetric encryption?...
✅ Added: What is the primary difference between symmetric and asymmetric encryption?...
✅ Added: What does SHA-256 stand for?...
✅ Added: What is the first step in incident response?...
✅ Added: Which of the following is NOT typically part of the incident response process?...
✅ Added: What is the purpose of containment in incident response?...

✨ Successfully added 18 sample questions to the database!
```

---

## Part 2: Running the Application

### Terminal 1: Start Backend Server
```bash
# From backend directory (already in there)
uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Terminal 2: Start Frontend Server
```bash
# Open new terminal/command prompt
cd c:\Users\SAMINATHAN\OneDrive\Desktop\h25-lms\frontend

# For Python 3:
python -m http.server 8080

# For Python 2:
python -m SimpleHTTPServer 8080
```

**Expected Output:**
```
Serving HTTP on 127.0.0.1 port 8080 (http://127.0.0.1:8080/) ...
```

### Step 3: Open in Browser
```
http://localhost:8080
```

---

## Part 3: Using the Application

### User Registration
1. Click "Register here" link
2. Fill in:
   - Email: your.email@example.com
   - Username: yourname
   - Password: securepassword123
   - Full Name (optional): Your Name
3. Click "Register" button
4. You'll be automatically logged in

### User Login
1. Enter Username
2. Enter Password
3. Click "Login" button
4. Redirected to Dashboard

### Dashboard
Shows your statistics:
- **Total Questions**: Number of questions answered
- **Accuracy**: Your percentage correct
- **Current Difficulty**: Your current difficulty level (1.0 - 5.0)
- **Current Streak**: Consecutive correct answers

**6 Topics Available:**
```
🐍 Python Basics
   → Learn Python fundamentals (lists, functions, data types)

🌐 Web Security
   → Secure web development (CSRF, SQL Injection, HTTPS)

📡 Networking
   → Network fundamentals (OSI model, TCP, HTTP)

🐧 Linux Security
   → Linux hardening (permissions, sudo, user management)

🔐 Cryptography
   → Encryption & security (AES, RSA, SHA-256)

🚨 Incident Response
   → Security incident handling (detection, containment, recovery)
```

### Starting a Quiz
1. Click on any topic card
2. Quiz page loads with first question
3. 10 questions will be asked from that topic

---

## Part 4: Quiz Experience

### Quiz Header (Top of Page)
```
┌────────────────────────────────────────────┐
│ 🐍 Python Basics                           │
│                                             │
│ 📊 Score: 0    🔥 Streak: 0    📈 1.0     │
│                                             │
│ Progress: 1/10 [████░░░░░░░░░░░░░░░░]     │
└────────────────────────────────────────────┘
```

### Question Display
```
┌────────────────────────────────────────────┐
│ Question 1                                  │
│                                             │
│ What is the correct way to create a list   │
│ in Python?                                  │
│                                             │
│ ⭕ A) my_list = [1, 2, 3, 4]              │
│ ⭕ B) my_list = (1, 2, 3, 4)              │
│ ⭕ C) my_list = {1, 2, 3, 4}              │
│ ⭕ D) my_list = <1, 2, 3, 4>              │
│                                             │
│ [Submit Answer] (disabled)                 │
└────────────────────────────────────────────┘
```

### How to Answer
1. **Read** the question carefully
2. **Click** on the option you think is correct (it highlights in blue)
3. The "Submit Answer" button becomes enabled
4. **Click** "Submit Answer"
5. System evaluates your answer

### After Submission
```
┌────────────────────────────────────────────┐
│ ✅ Correct!                                 │
│                                             │
│ Lists in Python are created using square   │
│ brackets []. Parentheses () create tuples, │
│ curly braces {} create sets, and angle     │
│ brackets <> are not used for collections.  │
│                                             │
│ [A) my_list = [1, 2, 3, 4]] (highlighted  │
│                                 in green)   │
└────────────────────────────────────────────┘

📊 Score: 10  🔥 Streak: 1  📈 1.0
```

Or if incorrect:
```
┌────────────────────────────────────────────┐
│ ❌ Incorrect!                               │
│                                             │
│ The correct answer is A. Lists use square  │
│ brackets...                                 │
│                                             │
│ [Your Answer - Red]  [A) Correct - Green]  │
└────────────────────────────────────────────┘

📊 Score: 0  🔥 Streak: 0  📈 1.0
```

### Auto-Progression
- After 2 seconds, next question automatically loads
- No need to click anything
- Progress bar updates
- Stats update

### Repeat for All Questions
- Questions 1-10 follow the same pattern
- Your score accumulates
- Difficulty adapts based on performance
- Streak resets to 0 if you answer incorrectly

---

## Part 5: Quiz Completion

### Question 10 Submission
After answering the 10th question, wait 2 seconds...

### Results Modal Appears
```
┌─────────────────────────────────────────┐
│            🎉 QUIZ COMPLETE!             │
│                                          │
│  Total Questions:        10              │
│  Correct Answers:        8  ✅           │
│  Score:                 80%  🏆          │
│  Time Taken:          4m 5s  ⏱️          │
│  New Difficulty:       1.5   📈          │
│                                          │
│  [Retake Quiz] [Back to Dashboard]       │
└─────────────────────────────────────────┘
```

### What the Stats Mean
- **Total Questions**: 10 (always for complete quiz)
- **Correct Answers**: How many you got right (8/10)
- **Score**: Percentage correct (8÷10 = 80%)
- **Time Taken**: How long quiz took (4 minutes 5 seconds)
- **New Difficulty**: Your new difficulty level (1.5, was 1.0)

### After Completion

**Option 1: Retake Quiz**
- Click "Retake Quiz"
- Starts a new quiz session with same topic
- Different questions (shuffled from database)
- Score resets to 0

**Option 2: Back to Dashboard**
- Click "Back to Dashboard"
- Returns to topic selection
- Your stats updated:
  - Total Questions: 20 (10 + 10)
  - Accuracy: Recalculated based on all answers
  - Difficulty: Updated to 1.5
  - Streak: Reset to 0

---

## Part 6: Dashboard Updates After Quiz

### Before Quiz
```
Total Questions: 0
Accuracy: 0%
Difficulty: 1.0
Streak: 0
```

### After First Quiz (8/10 Correct)
```
Total Questions: 10
Accuracy: 80%
Difficulty: 1.5  ← Increased (you did well)
Streak: 0        ← Reset after completing
```

### After Second Quiz (6/10 Correct)
```
Total Questions: 20   ← Accumulated
Accuracy: 70%        ← (14 correct out of 20)
Difficulty: 1.3      ← Decreased (harder questions didn't go as well)
Streak: 0
```

---

## Part 7: Scoring & Difficulty Explained

### Scoring System
```
Points per Question:
- Correct Answer: +10 points
- Incorrect Answer: 0 points

Total Score = (Correct Answers / Total Questions) × 100%

Examples:
- 10 correct / 10 questions = 100%
- 8 correct / 10 questions = 80%
- 5 correct / 10 questions = 50%
```

### Difficulty Adaptation
```
How it works:
- You start at Difficulty 1.0
- Answer correctly → Difficulty might increase (1.1, 1.2, etc.)
- Answer incorrectly → Difficulty might decrease (0.9, 0.8, etc.)
- Questions get harder as you do well
- Questions get easier if you struggle
- Range: 1.0 (Easiest) to 5.0 (Hardest)

Example Progression:
Q1: Correct   → Difficulty: 1.0 (no change yet)
Q2: Correct   → Difficulty: 1.0 (building streak)
Q3: Correct   → Difficulty: 1.1 (streak ≥ 3, increase)
Q4: Wrong     → Difficulty: 1.0 (streak broken, decrease)
Q5: Correct   → Difficulty: 1.0 (rebuilding)
...
```

### Streak System
```
What is a Streak?
- Number of consecutive correct answers
- Resets to 0 when you answer incorrectly

Example:
Q1: Correct   → Streak: 1
Q2: Correct   → Streak: 2
Q3: Correct   → Streak: 3 ← Good!
Q4: Wrong     → Streak: 0 ← Reset
Q5: Correct   → Streak: 1 ← Start over
```

---

## Part 8: Features Summary

✅ **MCQ Format**
- Exactly 4 options per question
- Only one correct answer
- Clear option labels (A, B, C, D)

✅ **Immediate Feedback**
- Correct answers shown in green
- Incorrect answers shown in red
- Full explanation provided
- Score updated instantly

✅ **Progress Tracking**
- Visual progress bar
- Question number display
- Real-time stats update
- Overall dashboard statistics

✅ **Adaptive Learning**
- Difficulty adjusts based on performance
- Easier questions if struggling
- Harder questions if doing well
- Personalized experience

✅ **User Experience**
- Smooth animations
- Auto-progression
- Exit confirmation
- Retake option
- Mobile responsive

---

## Part 9: Troubleshooting

### Issue: Page shows "Loading question..."
**Solution:**
1. Check backend is running: `uvicorn app.main:app --reload`
2. Check frontend is running: `python -m http.server 8080`
3. Press F12 to open developer console
4. Look for errors in console
5. Refresh page

### Issue: "Quiz session invalid"
**Solution:**
1. Start new quiz from dashboard
2. Don't leave quiz page open for very long
3. Complete quiz in one session

### Issue: No questions appear
**Solution:**
```bash
# Run this from backend directory:
python seed_questions.py

# Should show 18 questions added
```

### Issue: CORS error
**Solution:**
- Verify backend running on port 8000
- Verify frontend running on port 8080
- Clear browser cache (Ctrl+Shift+Delete)
- Restart both servers

### Issue: Can't register/login
**Solution:**
1. Check backend is running
2. Check database file exists (app.db)
3. Check console for error messages
4. Try different username/password

---

## Part 10: Technical Details

### API Endpoints Used
```
POST /api/quiz/start
  → Starts quiz session
  ← Returns first question

POST /api/quiz/answer?session_id=<id>
  → Submits answer
  ← Returns feedback + next question

POST /api/quiz/complete?session_id=<id>
  → Finishes quiz
  ← Returns final results

GET /api/quiz/topics
  → Gets available topics
```

### Question Structure
```json
{
    "question_id": 1,
    "question_text": "What is...",
    "options": [
        {"id": 1, "text": "Option A"},
        {"id": 2, "text": "Option B"},
        {"id": 3, "text": "Option C"},
        {"id": 4, "text": "Option D"}
    ],
    "correct_option_id": 1,
    "explanation": "This is why...",
    "difficulty": 1.0,
    "topic": "python_basics"
}
```

### Answer Submission
```json
{
    "question_id": 1,
    "selected_option_id": 1
}
```

### Response
```json
{
    "is_correct": true,
    "correct_option_id": 1,
    "explanation": "Lists are created with []...",
    "points_earned": 10,
    "current_score": 10,
    "current_streak": 1,
    "new_difficulty": 1.1,
    "next_question": { ... },
    "quiz_complete": false
}
```

---

## Part 11: Best Practices

### For Users
1. **Read carefully** - Don't rush through questions
2. **Take your time** - No time limit on questions
3. **Learn from mistakes** - Read explanations
4. **Retake quizzes** - Improve your score
5. **Try different topics** - Expand knowledge

### For Administrators
1. **Add questions regularly** - Keep content fresh
2. **Monitor difficulty** - Check if too easy/hard
3. **Review feedback** - Ensure explanations are clear
4. **Test regularly** - Verify all features work
5. **Backup database** - Don't lose question data

---

## Part 12: Quick Reference

### Keyboard Shortcuts
```
F12 - Open developer console (for debugging)
Ctrl+R - Refresh page
Ctrl+Shift+Delete - Clear cache
```

### File Locations
```
Backend: c:\Users\SAMINATHAN\OneDrive\Desktop\h25-lms\backend
Frontend: c:\Users\SAMINATHAN\OneDrive\Desktop\h25-lms\frontend
Database: backend/app.db (SQLite)
```

### Important Ports
```
Backend API: http://localhost:8000
Frontend: http://localhost:8080
API Docs: http://localhost:8000/docs
```

### Default Topics
```
python_basics (3 questions)
web_security (3 questions)
networking (3 questions)
linux_security (3 questions)
cryptography (3 questions)
incident_response (3 questions)
```

---

## 🎯 Quick Start (TL;DR)

```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate
python seed_questions.py
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
python -m http.server 8080

# Browser
http://localhost:8080
```

---

## ✨ You're Ready!

Everything is set up and ready to use. Start with:
1. Register a new account
2. Login to dashboard
3. Select any topic
4. Take a 10-question quiz
5. See your results

**Enjoy the Quiz Mode!** 🎓📝✅

---

**Created**: 2024
**Version**: 1.0.0
**Status**: Production Ready
