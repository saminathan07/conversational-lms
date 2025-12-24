# 🔐 Conversational LMS - AI-Powered Cybersecurity Training

An adaptive, AI-powered Learning Management System designed to train employees on cybersecurity through engaging conversational interactions. The platform dynamically adjusts question difficulty based on user performance, creating a personalized learning experience.

## ✨ Features

- 🤖 **AI-Powered Questions** - Dynamic question generation using Claude AI
- 📈 **Adaptive Difficulty** - Automatically adjusts complexity based on performance
- 🎯 **Multiple Topics** - Covers phishing, passwords, malware, social engineering, and more
- 📊 **Progress Tracking** - Real-time analytics and performance metrics
- 🔥 **Streak System** - Gamification to maintain engagement
- 💬 **Conversational UI** - Natural chat-based learning interface
- 🔒 **Secure Authentication** - JWT-based user authentication

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Anthropic API Key (optional - has fallback questions)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/sst-cloud-solutions/h25-lms
cd h25-lms
```

2. **Create environment file:**
```bash
cp .env.example .env
```

3. **Edit `.env` and add your API key:**
```env
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
SECRET_KEY=your-random-secret-key-minimum-32-characters
```

4. **Start all services:**
```bash
docker-compose up -d
```

5. **Access the application:**
- 🌐 Frontend: http://localhost:3000
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

### First Time Setup

1. Open http://localhost:3000
2. Click "Register here" 
3. Create an account
4. Choose a topic and start learning!

## 📁 Project Structure
```
h25-lms/
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── api/            # API route handlers
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── db/             # Database configuration
│   │   └── utils/          # Utility functions
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/               # Vanilla JS frontend
│   ├── index.html         # Login page
│   ├── dashboard.html     # User dashboard
│   ├── chat.html          # Learning interface
│   ├── css/               # Stylesheets
│   └── js/                # JavaScript logic
│
├── docs/                  # Documentation
├── docker-compose.yml     # Docker orchestration
├── .env.example          # Environment template
└── README.md
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **AI**: Anthropic Claude API

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients
- **Vanilla JavaScript** - No frameworks
- **Fetch API** - REST communication

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Frontend web server

## 🔧 Development

### Run without Docker

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
python -m http.server 3000
# Or use any static file server
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Claude API key | None (uses