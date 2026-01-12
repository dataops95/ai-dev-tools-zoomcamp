import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test health check returns 200"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestVideoProcessEndpoint:
    """Test video processing endpoint"""
    
    @patch('app.routers.videos.generate_summary_and_chapters')
    @patch('app.routers.videos.get_video_transcript')
    @patch('app.routers.videos.extract_video_id')
    def test_successful_video_processing(
        self,
        mock_extract_id,
        mock_get_transcript,
        mock_generate_summary
    ):
        """Test successful video processing"""
        # Setup mocks
        mock_extract_id.return_value = "test_video_id"
        mock_get_transcript.return_value = "Test transcript content"
        mock_generate_summary.return_value = {
            "summary": "This is a test summary",
            "chapters": [
                {
                    "timestamp": "00:00:00",
                    "title": "Introduction",
                    "description": "Video starts"
                }
            ]
        }
        
        # Make request
        response = client.post(
            "/api/videos/process",
            json={
                "youtube_url": "https://www.youtube.com/watch?v=test_video_id",
                "gemini_api_key": "test_api_key"
            }
        )
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "chapters" in data
        assert data["summary"] == "This is a test summary"
        assert len(data["chapters"]) == 1
    
    def test_invalid_youtube_url(self):
        """Test with invalid YouTube URL"""
        response = client.post(
            "/api/videos/process",
            json={
                "youtube_url": "https://invalid-url.com",
                "gemini_api_key": "test_api_key"
            }
        )
        
        assert response.status_code == 400
        assert "Invalid YouTube URL" in response.json()["detail"]
    
    @patch('app.routers.videos.get_video_transcript')
    @patch('app.routers.videos.extract_video_id')
    def test_transcript_not_available(self, mock_extract_id, mock_get_transcript):
        """Test when transcript is not available"""
        mock_extract_id.return_value = "test_video_id"
        mock_get_transcript.side_effect = Exception("Transcript not available")
        
        response = client.post(
            "/api/videos/process",
            json={
                "youtube_url": "https://www.youtube.com/watch?v=test_video_id",
                "gemini_api_key": "test_api_key"
            }
        )
        
        assert response.status_code == 400
    
    @patch('app.routers.videos.generate_summary_and_chapters')
    @patch('app.routers.videos.get_video_transcript')
    @patch('app.routers.videos.extract_video_id')
    def test_gemini_api_error(
        self,
        mock_extract_id,
        mock_get_transcript,
        mock_generate_summary
    ):
        """Test when Gemini API fails"""
        mock_extract_id.return_value = "test_video_id"
        mock_get_transcript.return_value = "Test transcript"
        mock_generate_summary.side_effect = Exception("API Error")
        
        response = client.post(
            "/api/videos/process",
            json={
                "youtube_url": "https://www.youtube.com/watch?v=test_video_id",
                "gemini_api_key": "test_api_key"
            }
        )
        
        assert response.status_code == 500
        assert "Failed to generate summary" in response.json()["detail"]
    
    def test_missing_required_fields(self):
        """Test request with missing required fields"""
        response = client.post(
            "/api/videos/process",
            json={"youtube_url": "https://www.youtube.com/watch?v=test"}
        )
        
        assert response.status_code == 422  # Unprocessable Entity
