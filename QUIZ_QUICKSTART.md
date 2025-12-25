# Quiz Mode - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Backend Setup
```bash
cd backend

# Activate virtual environment
venv\Scripts\activate

# Seed sample questions
python seed_questions.py
```

### Step 2: Start Backend
```bash
# Keep the backend running
uvicorn app.main:app --reload
# Backend runs on http://localhost:8000
```

### Step 3: Start Frontend (in a new terminal)
```bash
cd frontend
# Serve the frontend (or use any HTTP server)
# For Python 3:
python -m http.server 8080
# For Python 2:
python -m SimpleHTTPServer 8080
```

### Step 4: Open in Browser
```
http://localhost:8080
```

---

## 📝 User Workflow

1. **Register** → Fill in email, username, password
2. **Login** → Enter credentials
3. **Dashboard** → See stats and 6 topic options
4. **Select Topic** → Click any topic to start quiz
5. **Quiz** → Answer 10 MCQ questions
6. **Results** → See final score and statistics

---

## ❓ Quiz Mode Features

✨ **What You'll Experience:**

- **4 MCQ Options** per question (A, B, C, D)
- **Instant Feedback** - See if correct/wrong immediately
- **Explanations** - Why is the answer correct?
- **Score Tracking** - Points accumulate per correct answer
- **Streak Counter** - Consecutive correct answers
- **Difficulty Adaptation** - Adjusts based on performance
- **Auto-Progression** - Next question loads automatically
- **Final Results** - Complete statistics at quiz end

---

## 🎯 Sample Topics

| Topic | Focus Area |
|-------|-----------|
| 🐍 Python Basics | Variables, functions, data types |
| 🌐 Web Security | CSRF, SQL Injection, HTTPS |
| 📡 Networking | OSI model, TCP/IP, ports |
| 🐧 Linux Security | Permissions, sudo, user management |
| 🔐 Cryptography | AES, RSA, SHA-256 |
| 🚨 Incident Response | Detection, containment, recovery |

---

## 📊 Scoring System

- **Points per Question**: 10 points for correct
- **Streak Bonus**: Consecutive correct answers increase difficulty
- **Difficulty Levels**: 1.0 - 5.0 (adapts based on performance)
- **Final Score**: (Correct Answers / Total Questions) × 100%

---

## 🔧 Testing the API

### Start a Quiz
```bash
curl -X POST http://localhost:8000/api/quiz/start \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "python_basics",
    "number_of_questions": 10
  }'
```

### Submit an Answer
```bash
curl -X POST "http://localhost:8000/api/quiz/answer?session_id=YOUR_SESSION_ID" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": 1,
    "selected_option_id": 1
  }'
```

### Complete Quiz
```bash
curl -X POST "http://localhost:8000/api/quiz/complete?session_id=YOUR_SESSION_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🐛 Common Issues

### Issue: Quiz page shows "Loading question..."
**Solution**: 
- Make sure backend is running (`uvicorn app.main:app --reload`)
- Check browser console for errors (F12)
- Verify you're logged in

### Issue: No questions available
**Solution**:
```bash
python seed_questions.py
# Run from backend directory
```

### Issue: "Invalid quiz session" error
**Solution**:
- Refresh page and start quiz again
- Make sure you didn't leave quiz page open for too long

### Issue: CORS errors
**Solution**:
- Make sure backend CORS is enabled in `app/config.py`
- Check frontend is connecting to correct API URL

---

## 📱 Features Overview

### Question Display
- Clear question text
- 4 clickable options (A, B, C, D)
- Progress bar showing current question
- Score, streak, difficulty in header

### Answer Feedback
- Green highlight for correct answer
- Red highlight for incorrect selection
- Detailed explanation provided
- Correct option always shown

### Results Summary
- Total questions answered
- Number of correct answers
- Score percentage
- Time taken
- New difficulty level

---

## 🎮 How to Play

1. **Read** the question carefully
2. **Click** on the option you think is correct
3. **Submit** by clicking "Submit Answer" button
4. **Review** the explanation
5. **Proceed** to the next question (automatic)
6. **Finish** all 10 questions
7. **View** final results and statistics

---

## 💾 Database

Sample questions are provided with seed script:
- 18 pre-loaded MCQ questions
- 3 questions per topic
- Mix of difficulty levels
- Realistic exam-style questions

Add more questions:
1. Edit `backend/seed_questions.py`
2. Add to `SAMPLE_QUESTIONS` dict
3. Run `python seed_questions.py` again

---

## 📈 Next Steps

After taking a quiz:
- **Retake** the same topic to improve score
- **Try different** topic for variety
- **Check** dashboard for overall progress
- **Monitor** difficulty level growth

---

## 🆘 Help & Support

**Check Logs:**
```bash
# Terminal 1: Backend logs
uvicorn app.main:app --reload

# Terminal 2: Check frontend console
Press F12 → Console tab
```

**Debug Mode:**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Attempt quiz action
4. Check API response status and content

**Contact:**
Check `QUIZ_MODE_README.md` for detailed documentation

---

## 📚 What's Included

✅ Complete backend API with quiz endpoints
✅ Beautiful frontend quiz interface
✅ Real-time score and difficulty tracking
✅ 18 sample MCQ questions (3 per topic)
✅ Automatic question generation (via Claude AI)
✅ Session management and results tracking
✅ Mobile-responsive design
✅ Comprehensive documentation

---

**Ready to Quiz?** 🎯

1. Run `seed_questions.py` ✨
2. Start backend: `uvicorn app.main:app --reload` 🚀
3. Start frontend: `python -m http.server 8080` 📡
4. Open browser: `http://localhost:8080` 🌐
5. Register & Login 🔐
6. Click a topic and start quizzing! 📝

---

*Created: 2024*  
*Status: Ready to Use* ✨
