import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestIntegration:
    """Integration tests for the full video processing flow"""
    
    @patch('app.services.gemini.genai.GenerativeModel')
    @patch('app.services.gemini.genai.configure')
    @patch('app.services.transcript.YouTubeTranscriptApi.get_transcript')
    def test_full_video_processing_flow(
        self,
        mock_get_transcript,
        mock_gemini_configure,
        mock_gemini_model_class
    ):
        """Test the complete flow from URL input to summary output"""
        # Mock transcript API
        mock_get_transcript.return_value = [
            {'text': 'Welcome to this video.', 'start': 0.0, 'duration': 2.0},
            {'text': 'Today we will discuss important topics.', 'start': 2.0, 'duration': 3.0},
        ]
        
        # Mock Gemini API
        mock_response = MagicMock()
        mock_response.text = """{
            "summary": "This video discusses important topics in a comprehensive manner.",
            "chapters": [
                {
                    "timestamp": "00:00:00",
                    "title": "Introduction",
                    "description": "Welcome and overview"
                },
                {
                    "timestamp": "00:00:05",
                    "title": "Main Discussion",
                    "description": "Detailed topic exploration"
                }
            ]
        }"""
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_gemini_model_class.return_value = mock_model
        
        # Make request
        response = client.post(
            "/api/videos/process",
            json={
                "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "gemini_api_key": "test_api_key_12345"
            }
        )
        
        # Assertions
        assert response.status_code == 200
        
        data = response.json()
        assert "video_title" in data
        assert "duration" in data
        assert "summary" in data
        assert "chapters" in data
        
        # Verify summary
        assert "important topics" in data["summary"]
        
        # Verify chapters
        assert len(data["chapters"]) == 2
        assert data["chapters"][0]["title"] == "Introduction"
        assert data["chapters"][1]["title"] == "Main Discussion"
        
        # Verify mocks were called
        mock_get_transcript.assert_called_once_with("dQw4w9WgXcQ")
        mock_gemini_configure.assert_called_once_with(api_key="test_api_key_12345")
        assert mock_model.generate_content.called
