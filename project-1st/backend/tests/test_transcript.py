import pytest
from unittest.mock import patch, MagicMock
from app.services.transcript import (
    extract_video_id,
    get_video_transcript,
    get_transcript_with_timestamps
)


class TestExtractVideoId:
    """Test video ID extraction from various URL formats"""
    
    def test_standard_youtube_url(self):
        """Test standard youtube.com/watch URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_short_youtube_url(self):
        """Test short youtu.be URL"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_url_with_parameters(self):
        """Test URL with additional parameters"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=share"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_embed_url(self):
        """Test embed URL format"""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_invalid_url(self):
        """Test invalid URL raises ValueError"""
        url = "https://invalid-url.com/video"
        with pytest.raises(ValueError):
            extract_video_id(url)


class TestGetVideoTranscript:
    """Test transcript fetching"""
    
    @patch('app.services.transcript.YouTubeTranscriptApi.get_transcript')
    def test_successful_transcript_fetch(self, mock_get_transcript):
        """Test successful transcript retrieval"""
        # Mock transcript data
        mock_transcript = [
            {'text': 'Hello', 'start': 0.0, 'duration': 1.0},
            {'text': 'World', 'start': 1.0, 'duration': 1.0},
        ]
        mock_get_transcript.return_value = mock_transcript
        
        result = get_video_transcript("test_video_id")
        
        assert result == "Hello World"
        mock_get_transcript.assert_called_once_with("test_video_id")
    
    @patch('app.services.transcript.YouTubeTranscriptApi.get_transcript')
    def test_transcript_not_available(self, mock_get_transcript):
        """Test handling of unavailable transcript"""
        mock_get_transcript.side_effect = Exception("Transcript not available")
        
        with pytest.raises(Exception) as exc_info:
            get_video_transcript("test_video_id")
        
        assert "Could not retrieve transcript" in str(exc_info.value)


class TestGetTranscriptWithTimestamps:
    """Test transcript with timestamps fetching"""
    
    @patch('app.services.transcript.YouTubeTranscriptApi.get_transcript')
    def test_successful_fetch_with_timestamps(self, mock_get_transcript):
        """Test successful transcript with timestamps retrieval"""
        mock_transcript = [
            {'text': 'Hello', 'start': 0.0, 'duration': 1.0},
            {'text': 'World', 'start': 1.0, 'duration': 1.0},
        ]
        mock_get_transcript.return_value = mock_transcript
        
        result = get_transcript_with_timestamps("test_video_id")
        
        assert result == mock_transcript
        assert len(result) == 2
        mock_get_transcript.assert_called_once_with("test_video_id")
