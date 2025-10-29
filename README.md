# AI Campus Admin - Backend API

## Overview
FastAPI backend with LangGraph AI agent for campus administration, featuring student management, chat history, analytics, and authentication.

## Features
- 🤖 AI-powered chat assistant with LangGraph
- 👥 Student management (CRUD operations)
- 📊 Analytics and reporting
- 💬 Chat history tracking
- 🔐 JWT authentication & authorization
- 🎤 Voice interaction support (optional)
- 📧 Email notifications (optional)

## Tech Stack
- **Framework**: FastAPI
- **Database**: MongoDB (Motor async driver)
- **AI**: LangChain + OpenAI
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib with bcrypt

## Quick Start

### Local Development

1. **Install Dependencies**:
```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install -r requirements.txt
```

2. **Set Up Environment**:
```bash
# Copy example env file
cp env.example .env

# Edit .env with your values
nano .env
```

3. **Run MongoDB** (if local):
```bash
mongod --dbpath /path/to/data
```

4. **Start Server**:
```bash
# Using Poetry
poetry run uvicorn main:app --reload

# Or directly
uvicorn main:app --reload
```

5. **Access API**:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Deployment

See [README_DEPLOYMENT.md](README_DEPLOYMENT.md) for detailed Hugging Face Spaces deployment instructions.

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user
- `PUT /auth/me` - Update profile

### Chat
- `POST /chat/authenticated` - Chat with AI (authenticated)
- `GET /stream` - Stream AI responses
- `GET /history/me` - Get my chat history
- `DELETE /history/me` - Delete my chat history

### Students
- `GET /students/` - List all students
- `POST /students/` - Create student
- `GET /students/{id}` - Get student
- `PUT /students/{id}` - Update student
- `DELETE /students/{id}` - Delete student

### Analytics
- `GET /analytics/` - Get analytics overview
- `GET /students/analytics/overview` - Student analytics

## Environment Variables

Required:
- `OPENAI_API_KEY` - OpenAI API key
- `MONGODB_URI` - MongoDB connection string
- `JWT_SECRET_KEY` - JWT secret (min 32 chars)

Optional:
- `MONGODB_DB` - Database name (default: ai_campus)
- `ELEVENLABS_API_KEY` - For voice features
- `SMTP_USERNAME` - For email notifications
- `SMTP_PASSWORD` - Email password
- `ALLOW_ORIGINS` - CORS allowed origins

## Project Structure
```
backend/
├── main.py              # FastAPI application entry point
├── settings.py          # Configuration & environment
├── db.py               # Database connection
├── schemas.py          # Pydantic models
├── models/             # Database models
│   ├── user.py
│   └── student.py
├── routers/            # API endpoints
│   ├── auth.py
│   ├── chat.py
│   ├── students.py
│   └── analytics.py
├── services/           # Business logic
│   ├── auth.py
│   ├── users.py
│   ├── students.py
│   └── chat_history.py
├── agent/              # LangGraph AI agent
│   ├── graph.py
│   ├── tools.py
│   └── ragagent.py
└── uaf_data/           # Custom data
```

## Development

### Run Tests
```bash
poetry run pytest
```

### Code Formatting
```bash
poetry run black .
poetry run ruff check .
```

### Create Admin User
```bash
poetry run python scripts/create_admin.py
```

## License
MIT

## Support
For issues and questions, please open an issue on the repository.

