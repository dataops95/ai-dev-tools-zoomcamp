# Quick Start Guide

## Getting Started in 5 Minutes

### Prerequisites
- Docker and Docker Compose installed
- Google Gemini API key ([Get one free here](https://makersuite.google.com/app/apikey))

### Step 1: Clone and Start
```bash
git clone <repository-url>
cd ai-dev-tools-zoomcamp/project-1st
docker compose up --build
```

Wait for both services to start (about 1-2 minutes).

### Step 2: Access the Application
Open your browser and go to: **http://localhost:5173**

### Step 3: Get Your Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated key

### Step 4: Process a Video
1. **Paste a YouTube URL** (try this one for testing):
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

2. **Enter your Gemini API key** in the password field

3. **Click "Summarize Video"**

4. **Wait 10-30 seconds** for processing (depending on video length)

5. **View Results**:
   - Video summary (3-5 sentences)
   - Chapter breakdown with timestamps
   - Copy buttons for easy sharing

### Step 5: Explore Features
- ✨ Copy individual chapters
- 📋 Copy all content at once
- 🔄 Try different videos
- 📱 Works on mobile too!

## Supported YouTube URLs
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID&feature=...`
- `https://www.youtube.com/embed/VIDEO_ID`

## Troubleshooting

### "Transcript not available"
- Not all videos have transcripts/captions
- Try videos with auto-generated captions
- Private videos won't work

### "API Error"
- Check your Gemini API key is correct
- Verify you have API quota remaining
- Try again in a few seconds

### Docker Issues
```bash
# Stop containers
docker compose down

# Rebuild from scratch
docker compose up --build --force-recreate
```

## Testing Without Docker

### Backend
```bash
cd backend
pip install -r requirements.txt
pytest -v  # Run tests
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm test   # Run tests
npm run dev
```

## API Documentation
Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Videos to Try
1. **Short tutorial** (3-5 min): Great for testing
2. **Tech talk** (10-20 min): Good chapter breakdown
3. **Educational video** (5-15 min): Best summaries

## Stop the Application
```bash
docker compose down
```

## Need Help?
- Check **README.md** for detailed documentation
- See **AGENTS.md** for development insights
- Review **PROJECT_SUMMARY.md** for implementation details

---

**Enjoy summarizing videos with AI! 🎬🤖**
