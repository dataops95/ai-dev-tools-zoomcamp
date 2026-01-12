# YouTube Video Summarizer

An AI-powered web application that extracts transcripts from YouTube videos and generates intelligent summaries with chapter breakdowns using Google Gemini API.

## Problem Description

Content creators and learners often need to quickly understand the content of long YouTube videos without watching the entire video. This tool solves that problem by:

- **Extracting transcripts** automatically from YouTube videos (no API key needed)
- **Generating AI-powered summaries** that capture the key points in 3-5 sentences
- **Creating chapter breakdowns** with timestamps, titles, and descriptions for easy navigation
- **Providing copy-to-clipboard functionality** for easy sharing and note-taking

## System Functionality

The YouTube Video Summarizer is a full-stack web application that:

1. **Accepts YouTube video URLs** in various formats (youtube.com/watch, youtu.be, etc.)
2. **Extracts video transcripts** using the youtube-transcript-api library
3. **Processes transcripts** with Google Gemini AI to generate:
   - Concise summary of the video content
   - Chapter breakdown with timestamps and descriptions
4. **Displays results** in a user-friendly interface with copy functionality
5. **Handles errors gracefully** with clear user feedback

## Technology Stack

### Frontend
- **React 18** - Modern UI library for building interactive interfaces
- **Vite** - Fast build tool and development server
- **TailwindCSS** - Utility-first CSS framework for responsive design
- **Vitest** - Fast unit testing framework for React components
- **Testing Library** - Testing utilities for React components

### Backend
- **FastAPI** - High-performance Python web framework
- **Python 3.11** - Programming language with modern features
- **youtube-transcript-api** - Library for extracting YouTube transcripts
- **google-generativeai** - Official Google Gemini API SDK
- **Pydantic** - Data validation using Python type annotations
- **pytest** - Testing framework for Python

### AI/ML
- **Google Gemini Pro** - Large language model for text generation and summarization

### Containerization
- **Docker** - Container platform for consistent deployments
- **docker-compose** - Multi-container orchestration for local development
- **nginx** - Web server for serving frontend static files

### CI/CD
- **GitHub Actions** - Automated testing and deployment pipeline
- **Docker Hub** - Container registry for storing images
- **Render** - Cloud platform for deployment (optional)

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
│                      (React + Vite App)                      │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/JSON
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  /api/videos/process endpoint                        │  │
│  └─────┬─────────────────────────────┬──────────────────┘  │
│        │                              │                      │
│        ▼                              ▼                      │
│  ┌──────────────┐            ┌──────────────┐              │
│  │  Transcript   │            │   Gemini AI  │              │
│  │   Service     │            │   Service    │              │
│  └──────┬───────┘            └──────┬───────┘              │
│         │                             │                      │
└─────────┼─────────────────────────────┼──────────────────────┘
          │                             │
          ▼                             ▼
  ┌───────────────┐           ┌─────────────────┐
  │   YouTube     │           │  Google Gemini  │
  │  Transcript   │           │      API        │
  │     API       │           │                 │
  └───────────────┘           └─────────────────┘
```

**Data Flow:**
1. User enters YouTube URL and Gemini API key in frontend
2. Frontend sends POST request to `/api/videos/process`
3. Backend extracts video ID and fetches transcript from YouTube
4. Backend sends transcript to Gemini API for summarization
5. Gemini returns structured summary and chapters
6. Backend returns formatted response to frontend
7. Frontend displays results with copy-to-clipboard functionality

## Setup Instructions

### Prerequisites
- Docker and docker-compose installed
- (Optional) Node.js 20+ and Python 3.11+ for local development
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Local Development with Docker Compose

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ai-dev-tools-zoomcamp/project-1st
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

### Local Development without Docker

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Codespaces Setup

1. Open the repository in GitHub Codespaces
2. The devcontainer will automatically set up the environment
3. Dependencies will be installed via `postCreateCommand`
4. Ports 5173 (frontend) and 8000 (backend) will be forwarded
5. Run the application:
   ```bash
   # Terminal 1 - Backend
   cd project-1st/backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2 - Frontend
   cd project-1st/frontend
   npm run dev
   ```

### Environment Variables

**Backend (.env):**
```bash
CORS_ORIGINS=http://localhost:5173,http://localhost
LOG_LEVEL=INFO
MAX_TRANSCRIPT_LENGTH=100000
API_TIMEOUT=60
```

**Frontend (.env):**
```bash
VITE_API_BASE_URL=http://localhost:8000
```

## Running Tests

### Backend Tests
```bash
cd backend
pytest -v
```

Test coverage includes:
- Transcript extraction service tests
- Gemini API integration tests
- API endpoint tests
- Integration tests for full flow

### Frontend Tests
```bash
cd frontend
npm test
```

Test coverage includes:
- VideoInput component validation tests
- SummaryDisplay rendering tests
- API service tests with mocked fetch

## Deployment

### Building Docker Images

**Backend:**
```bash
cd backend
docker build -t youtube-summarizer-backend .
```

**Frontend:**
```bash
cd frontend
docker build -t youtube-summarizer-frontend .
```

### Deploying to Render

1. **Create two Web Services on Render:**
   - Backend: Docker service using backend image
   - Frontend: Docker service using frontend image

2. **Configure Environment Variables:**
   - Backend: `CORS_ORIGINS` (include your frontend URL)
   - Frontend: `VITE_API_BASE_URL` (your backend URL)

3. **Set up GitHub Actions secrets:**
   - `DOCKER_HUB_USERNAME`
   - `DOCKER_HUB_TOKEN`
   - `RENDER_DEPLOY_HOOK_URL` (optional)

4. **Push to main branch:**
   - CI/CD pipeline will automatically test, build, and push images
   - Render will auto-deploy from Docker Hub (if configured)

### CI/CD Pipeline

The GitHub Actions workflow includes:

1. **Test Stage** (on push/PR):
   - Run backend pytest tests
   - Run frontend vitest tests
   - Fail if any tests don't pass

2. **Build Stage** (on push to main):
   - Build backend Docker image
   - Build frontend Docker image
   - Tag with commit SHA and 'latest'
   - Push to Docker Hub

3. **Deploy Stage** (on push to main):
   - Trigger Render deployment via webhook

## Usage

1. **Get a Gemini API Key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

2. **Open the Application:**
   - Navigate to http://localhost:5173 (or your deployed URL)

3. **Enter Video Details:**
   - Paste a YouTube video URL
   - Enter your Gemini API key
   - Click "Summarize Video"

4. **View Results:**
   - Read the generated summary
   - Browse chapter breakdown with timestamps
   - Use copy buttons to share or save content

5. **Supported YouTube URL Formats:**
   - `https://www.youtube.com/watch?v=VIDEO_ID`
   - `https://youtu.be/VIDEO_ID`
   - `https://www.youtube.com/embed/VIDEO_ID`

## API Documentation

The backend API follows the OpenAPI 3.0 specification defined in `openapi.yaml`.

**Key Endpoints:**

- `GET /api/health` - Health check endpoint
- `POST /api/videos/process` - Process YouTube video and generate summary

**Interactive API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**OpenAPI Spec:** See `openapi.yaml` for complete API contract

## Project Structure

```
project-1st/
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # CI/CD pipeline
├── .devcontainer/
│   └── devcontainer.json          # Codespaces configuration
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   └── videos.py          # Video processing endpoints
│   │   ├── services/
│   │   │   ├── transcript.py      # YouTube transcript extraction
│   │   │   └── gemini.py          # Gemini API integration
│   │   ├── config.py              # Configuration settings
│   │   └── main.py                # FastAPI application
│   ├── tests/                     # Backend tests
│   ├── Dockerfile                 # Backend container
│   └── requirements.txt           # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── VideoInput.jsx     # URL input form
│   │   │   ├── SummaryDisplay.jsx # Results display
│   │   │   └── LoadingSpinner.jsx # Loading indicator
│   │   ├── services/
│   │   │   └── api.js             # API service layer
│   │   ├── __tests__/             # Frontend tests
│   │   ├── App.jsx                # Main application component
│   │   └── main.jsx               # Application entry point
│   ├── Dockerfile                 # Frontend container
│   ├── nginx.conf                 # Nginx configuration
│   └── package.json               # Node.js dependencies
├── docker-compose.yml             # Multi-container setup
├── openapi.yaml                   # API specification
├── README.md                      # This file
└── AGENTS.md                      # AI tools documentation
```

## Limitations & Future Enhancements

**Current Limitations:**
- Single video processing only (no batch processing)
- No user authentication or session management
- No database persistence (results not saved)
- Video title and duration not extracted (MVP simplification)
- Single-user design (no multi-tenancy)

**Future Enhancements:**
- User authentication and personal history
- Database persistence (Supabase/MongoDB)
- Playlist processing support
- MCP server integration
- Multi-language support
- Advanced topic segmentation
- Video caching to reduce API calls
- Real YouTube Data API integration for metadata

## Troubleshooting

**Transcript not available:**
- Not all YouTube videos have transcripts/captions
- Try videos with auto-generated captions enabled
- Private or age-restricted videos may not work

**Gemini API errors:**
- Verify your API key is valid
- Check API quota limits
- Ensure API key has proper permissions

**Docker issues:**
- Ensure Docker daemon is running
- Check port conflicts (5173, 8000)
- Try `docker-compose down -v` to reset volumes

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## License

This project is for educational purposes as part of the AI Dev Tools Zoomcamp.

## Support

For issues and questions:
- Check the [API Documentation](http://localhost:8000/docs)
- Review the [OpenAPI Specification](openapi.yaml)
- See [AGENTS.md](AGENTS.md) for AI-assisted development workflow