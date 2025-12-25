# Quiz Mode - Visual Documentation

## User Journey Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    QUIZ MODE USER FLOW                       │
└─────────────────────────────────────────────────────────────┘

STEP 1: Authentication
────────────────────
    index.html
        ↓
    ┌────────────────┐
    │ Register Form  │
    └────────┬───────┘
             │ (Create Account)
             ↓
    ┌────────────────┐
    │ Login Form     │
    └────────┬───────┘
             │ (Username + Password)
             ↓
    [JWT Token Stored]
             ↓
    ✅ Authenticated

STEP 2: Dashboard & Topic Selection
───────────────────────────────────
    dashboard.html
         ↓
    ┌──────────────────────┐
    │ Display User Stats   │
    │ - Total Questions    │
    │ - Accuracy %         │
    │ - Difficulty Level   │
    │ - Current Streak     │
    └────────┬─────────────┘
             │
    ┌────────▼──────────────────┐
    │  Load Topics from API      │
    │  GET /api/quiz/topics      │
    └────────┬──────────────────┘
             │
    ┌────────▼──────────────────────────┐
    │  Display 6 Topic Buttons           │
    │  - 🐍 Python Basics               │
    │  - 🌐 Web Security                │
    │  - 📡 Networking                  │
    │  - 🐧 Linux Security              │
    │  - 🔐 Cryptography                │
    │  - 🚨 Incident Response           │
    └────────┬───────────────────────────┘
             │ (Click Topic)
             ↓
    ✅ Topic Selected

STEP 3: Quiz Initialization
──────────────────────────
    quiz.html?topic=<topic_id>
         ↓
    [POST /api/quiz/start]
         ↓
    ┌──────────────────────┐
    │ Backend Creates:      │
    │ - Session ID (UUID)  │
    │ - Load 10 Questions  │
    │ - Set Difficulty     │
    │ - Record Start Time  │
    └────────┬─────────────┘
             │
    ✅ Session Created

STEP 4: Question Display
────────────────────────
    quiz.html
         ↓
    ┌────────────────────────────────────┐
    │         QUIZ HEADER                 │
    │  📊 Score: 0  🔥 Streak: 0  📈 1.0 │
    │  Progress: 1/10 [████░░░░░░░░]     │
    └─────────────────────────────────────┘
             ↓
    ┌─────────────────────────────────────┐
    │    Question 1 of 10                  │
    │                                      │
    │    What is the correct way to...?   │
    │                                      │
    │  ⭕ A) Option 1                     │
    │  ⭕ B) Option 2                     │
    │  ⭕ C) Option 3                     │
    │  ⭕ D) Option 4                     │
    │                                      │
    │  [Submit Answer] (disabled)          │
    └─────────────────────────────────────┘
             │ (Select Option)
             ↓
    ┌─────────────────────────────────────┐
    │  Option Selected → Highlighted       │
    │  [Submit Answer] (enabled)           │
    └─────────────────────────────────────┘
             │ (Click Submit)
             ↓
    ✅ Answer Submitted

STEP 5: Answer Evaluation
─────────────────────────
    [POST /api/quiz/answer]
         ↓
    Backend Processes:
    ┌──────────────────────────────┐
    │ 1. Check if Option Correct   │
    │ 2. Update Score (+10)        │
    │ 3. Update Streak             │
    │ 4. Adjust Difficulty         │
    │ 5. Save Response to DB       │
    │ 6. Load Next Question        │
    └──────────────────────────────┘
             ↓
    Response Contains:
    ┌──────────────────────────────┐
    │ is_correct: true/false       │
    │ explanation: "Why..."        │
    │ points_earned: 10            │
    │ current_score: 10            │
    │ current_streak: 1            │
    │ new_difficulty: 1.2          │
    │ next_question: {...}         │
    └──────────────────────────────┘
             ↓

STEP 6: Feedback Display
────────────────────────
    quiz.html Shows:
         ↓
    IF CORRECT:
    ┌──────────────────────────────┐
    │  ✅ Correct!                  │
    │  Explanation: This is why...  │
    │                               │
    │  (Green highlight)            │
    │  [A) Correct Answer]          │
    └──────────────────────────────┘
         ↓
    IF INCORRECT:
    ┌──────────────────────────────┐
    │  ❌ Incorrect!                │
    │  Explanation: Actually...     │
    │                               │
    │  [Your answer - Red]          │
    │  [A) Correct Answer - Green]  │
    └──────────────────────────────┘
             ↓
    Stats Update:
    ┌──────────────────────────────┐
    │  Score: 10    ← Updated       │
    │  Streak: 1    ← Updated       │
    │  Difficulty: 1.2 ← Updated    │
    └──────────────────────────────┘
             ↓
    [2 second delay]
             ↓

STEP 7: Auto-Progression
────────────────────────
    [Next question automatically loads]
         ↓
    Back to STEP 4 (Question Display)
    for Question 2/10, 3/10, ..., 10/10
             ↓
    Repeat until Question 10 completed
             ↓
    ✅ All Questions Answered

STEP 8: Quiz Completion
──────────────────────
    After Question 10:
         ↓
    [POST /api/quiz/complete]
         ↓
    Backend Calculates:
    ┌──────────────────────────────┐
    │ - Total Questions: 10        │
    │ - Correct Answers: 8         │
    │ - Incorrect: 2               │
    │ - Score %: 80%               │
    │ - Time Taken: 245 seconds    │
    │ - Final Difficulty: 1.5      │
    └──────────────────────────────┘
             ↓

STEP 9: Results Modal
────────────────────
    ┌──────────────────────────────────┐
    │   🎉 QUIZ COMPLETE!               │
    │                                   │
    │  Total Questions:     10          │
    │  Correct Answers:     8  ✅       │
    │  Score:              80%  🏆     │
    │  Time Taken:      4m 5s  ⏱️     │
    │  New Difficulty:     1.5  📈     │
    │                                   │
    │  [Retake Quiz]  [Back to Dashboard]│
    └──────────────────────────────────┘
             ↓
    User Choice:
    ├─ Retake Quiz → Back to STEP 3
    │              (Create new session)
    │
    └─ Dashboard → Back to STEP 2
                  (Topic selection)

STEP 10: Dashboard Update
────────────────────────
    Back on Dashboard:
         ↓
    ┌──────────────────────────────┐
    │ Stats Updated:               │
    │ - Total: 10 (+10)            │
    │ - Correct: 8 (+8)            │
    │ - Accuracy: 80% (updated)    │
    │ - Difficulty: 1.5 (updated)  │
    │ - Streak: 0 (session reset)  │
    └──────────────────────────────┘
             ↓
    User can:
    ├─ Select same topic to retake
    ├─ Select different topic
    └─ Logout
```

---

## API Communication Diagram

```
FRONTEND                          BACKEND
(Browser)                         (FastAPI)
   │                                 │
   │                                 │
   │─ POST /quiz/start ─────────────→│
   │  {topic, num_questions}         │
   │                                 │ ✓ Create Session
   │                                 │ ✓ Load Questions
   │←───── 200 OK ────────────────────│
   │  {session_id, first_question}   │
   │                                 │
   │  [Display Question]             │
   │  [User selects option]          │
   │                                 │
   │─ POST /quiz/answer ────────────→│
   │  {question_id, option_id}       │
   │                                 │ ✓ Evaluate
   │                                 │ ✓ Update Stats
   │                                 │ ✓ Load Next Q
   │←───── 200 OK ────────────────────│
   │  {is_correct, next_question}    │
   │                                 │
   │  [Display Feedback]             │
   │  [2 sec delay]                  │
   │  [Display Next Question]        │
   │                                 │
   │─ POST /quiz/answer ────────────→│
   │  {question_id, option_id}       │
   │                                 │ ✓ Evaluate
   │←───── 200 OK ────────────────────│
   │  {...next_question...}          │
   │                                 │
   │  ... (repeat for all 10 Qs) ... │
   │                                 │
   │─ POST /quiz/complete ─────────→│
   │  {session_id}                   │
   │                                 │ ✓ Calculate Results
   │←───── 200 OK ────────────────────│
   │  {score_pct, time, stats}       │
   │                                 │
   │  [Show Results Modal]           │
   │
```

---

## Database Schema (Question Model)

```sql
CREATE TABLE questions (
    id INT PRIMARY KEY,
    user_id INT,
    topic VARCHAR(100),
    difficulty FLOAT,
    
    -- Question Content
    question_text TEXT,
    
    -- MCQ Options (JSON)
    options JSON,  -- [
                   --   {"id": 1, "text": "Option A"},
                   --   {"id": 2, "text": "Option B"},
                   --   {"id": 3, "text": "Option C"},
                   --   {"id": 4, "text": "Option D"}
                   -- ]
    
    -- Correct Answer
    correct_option_id INT,
    correct_answer TEXT,
    explanation TEXT,
    
    created_at TIMESTAMP
);

Example Row:
┌────┬────────┬─────────┬───────────────────────────────┐
│ id │ topic  │ options │ correct_option_id             │
├────┼────────┼─────────┼───────────────────────────────┤
│ 1  │ python │ [{"id":1│ 1                             │
│    │        │ "text"  │                               │
│    │        │ "my_li  │                               │
│    │        │ st = [] │                               │
└────┴────────┴─────────┴───────────────────────────────┘
```

---

## Session Management

```
Session Storage (In-Memory):

active_sessions = {
    "uuid-1": {
        "user_id": 123,
        "topic": "python_basics",
        "questions": [1, 5, 12, 8, ...],
        "current_index": 3,
        "start_time": datetime(...),
        "answers": [
            {"question_id": 1, "selected_option_id": 1, "is_correct": true},
            {"question_id": 5, "selected_option_id": 2, "is_correct": false},
            {"question_id": 12, "selected_option_id": 3, "is_correct": true}
        ],
        "scores": 20
    },
    "uuid-2": { ... }
}

Note: For production, use Redis or database
```

---

## State Transitions

```
Quiz States:
┌──────────┐
│  START   │ ← User clicks topic
└────┬─────┘
     │
     ▼
┌─────────────────┐
│ IN_PROGRESS     │ ← Answering questions
└────┬────────────┘
     │ (Q1 → Q2 → Q3 → ... → Q10)
     │
     ▼
┌──────────────────┐
│ AWAITING_RESULT  │ ← Last question submitted
└────┬─────────────┘
     │ (2 second delay)
     │
     ▼
┌──────────────────┐
│ COMPLETE         │ ← Show results
└─────────────────┘
     │
     ├─ Retake
     │  (back to START)
     │
     └─ Dashboard
        (cleanup session)
```

---

## File Organization

```
PROJECT ROOT
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── quiz.py          ✨ NEW - Quiz endpoints
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   └── ...
│   │   │
│   │   ├── models/
│   │   │   ├── question.py      ✏️ MODIFIED - MCQ fields
│   │   │   ├── user.py
│   │   │   └── ...
│   │   │
│   │   ├── schemas/
│   │   │   ├── quiz_schema.py   ✨ NEW - Quiz models
│   │   │   └── ...
│   │   │
│   │   ├── services/
│   │   │   ├── ai_engine.py     ✏️ MODIFIED - MCQ generation
│   │   │   └── ...
│   │   │
│   │   ├── config.py
│   │   ├── main.py              ✏️ MODIFIED - Router added
│   │   └── ...
│   │
│   └── seed_questions.py        ✨ NEW - Database seeding
│
├── frontend/
│   ├── quiz.html                ✨ NEW - Quiz page
│   ├── dashboard.html           ✏️ MODIFIED - Topic buttons
│   ├── css/
│   │   ├── quiz.css            ✨ NEW - Quiz styles
│   │   ├── dashboard.css       ✏️ MODIFIED - Topic styling
│   │   └── main.css
│   └── js/
│       ├── quiz.js             ✨ NEW - Quiz logic
│       ├── api.js
│       └── ...
│
├── docs/
│   ├── architecture.md
│   └── ...
│
├── QUIZ_MODE_README.md          ✨ NEW - Detailed documentation
├── QUIZ_QUICKSTART.md           ✨ NEW - Quick start guide
└── IMPLEMENTATION_SUMMARY.md    ✨ NEW - This summary
```

---

## Scoring Calculation

```
Score = (Correct Answers / Total Questions) × 100

Example:
- Total Questions: 10
- Correct Answers: 8
- Incorrect Answers: 2
- Score: (8 / 10) × 100 = 80%

Points per Question:
- Correct: +10 points
- Incorrect: 0 points

Total Points = Number of Correct × 10
```

---

## Difficulty Adaptation

```
Initial Difficulty: 1.0

After Each Answer:
├─ If CORRECT
│  └─ Streak++
│     └─ If Streak > 2
│        └─ Difficulty += 0.1
│
└─ If INCORRECT
   └─ Streak = 0
      └─ Difficulty -= 0.1

Range: 1.0 ≤ Difficulty ≤ 5.0

Example:
Q1: Correct  → Streak: 1, Diff: 1.0
Q2: Correct  → Streak: 2, Diff: 1.0
Q3: Correct  → Streak: 3, Diff: 1.1  ⬆️
Q4: Wrong    → Streak: 0, Diff: 1.0  ⬇️
Q5: Correct  → Streak: 1, Diff: 1.0
...
```

---

## Component Interaction

```
┌─────────────────────────────────────────────┐
│           Frontend (Browser)                │
│  ┌─────────────────────────────────────┐   │
│  │      quiz.html                      │   │
│  │  ┌──────────────────────────────┐   │   │
│  │  │   Quiz Header                │   │   │
│  │  │   Progress Bar               │   │   │
│  │  │   Stats (Score, Streak, Diff)│   │   │
│  │  └──────────────────────────────┘   │   │
│  │  ┌──────────────────────────────┐   │   │
│  │  │   Question Display           │   │   │
│  │  │   4 Option Buttons           │   │   │
│  │  │   Submit Button              │   │   │
│  │  └──────────────────────────────┘   │   │
│  │  ┌──────────────────────────────┐   │   │
│  │  │   Feedback Message           │   │   │
│  │  │   Results Modal              │   │   │
│  │  └──────────────────────────────┘   │   │
│  └─────────────────────────────────────┘   │
│              ↑              ↓                │
│        quiz.js (Orchestrator)               │
│              ↑              ↓                │
│           api.js (HTTP calls)               │
└──────────────────┬──────────────────────────┘
                   │ HTTP
                   │ /api/quiz/*
                   ↓
┌─────────────────────────────────────────────┐
│         Backend (FastAPI)                   │
│  ┌─────────────────────────────────────┐   │
│  │    Quiz Router (quiz.py)            │   │
│  │  - /start (create session)          │   │
│  │  - /answer (evaluate & next Q)      │   │
│  │  - /complete (results)              │   │
│  │  - /topics (available)              │   │
│  └─────────────────────────────────────┘   │
│           ↓              ↓                   │
│     ┌──────────────┐  ┌──────────────┐     │
│     │ AI Engine    │  │ Adaptive     │     │
│     │ (generate Q) │  │ (difficulty) │     │
│     └──────────────┘  └──────────────┘     │
│           ↓              ↓                   │
│     ┌──────────────────────────────┐       │
│     │      Database (SQLite)       │       │
│     │  - Questions (MCQ)           │       │
│     │  - Responses (Answers)       │       │
│     │  - Users & Progress          │       │
│     └──────────────────────────────┘       │
└─────────────────────────────────────────────┘
```

---

## Error Handling

```
Quiz Error Scenarios:
├─ Invalid Session
│  └─ → Return 400: "Invalid quiz session"
│
├─ Question Not Found
│  └─ → Return 404: "Question not found"
│
├─ Unauthorized User
│  └─ → Return 403: "Not authorized for this session"
│
├─ API Error
│  └─ → Show fallback questions
│
└─ Network Error
   └─ → Show error message, retry option
```

---

This documentation provides:
✅ Complete visual flow of user journey
✅ API communication diagram
✅ Database schema
✅ Session management visualization
✅ State transitions
✅ File organization
✅ Scoring logic
✅ Difficulty adaptation
✅ Component interaction
✅ Error handling flow
