import pytest
from unittest.mock import patch, MagicMock
import json
from app.services.gemini import generate_summary_and_chapters


class TestGenerateSummaryAndChapters:
    """Test Gemini API integration"""
    
    @patch('app.services.gemini.genai.GenerativeModel')
    @patch('app.services.gemini.genai.configure')
    def test_successful_generation(self, mock_configure, mock_model_class):
        """Test successful summary and chapter generation"""
        # Mock response
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "summary": "This is a test summary of the video content.",
            "chapters": [
                {
                    "timestamp": "00:00:00",
                    "title": "Introduction",
                    "description": "Video introduction"
                },
                {
                    "timestamp": "00:05:30",
                    "title": "Main Content",
                    "description": "Main discussion"
                }
            ]
        })
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        # Test
        result = generate_summary_and_chapters("Test transcript", "test_api_key")
        
        # Assertions
        assert "summary" in result
        assert "chapters" in result
        assert len(result["chapters"]) == 2
        assert result["chapters"][0]["timestamp"] == "00:00:00"
        mock_configure.assert_called_once_with(api_key="test_api_key")
    
    @patch('app.services.gemini.genai.GenerativeModel')
    @patch('app.services.gemini.genai.configure')
    def test_json_in_markdown_codeblock(self, mock_configure, mock_model_class):
        """Test parsing JSON from markdown code block"""
        # Mock response with markdown
        mock_response = MagicMock()
        mock_response.text = """```json
{
  "summary": "Test summary",
  "chapters": [
    {"timestamp": "00:00:00", "title": "Start", "description": "Beginning"}
  ]
}
```"""
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        result = generate_summary_and_chapters("Test transcript", "test_api_key")
        
        assert "summary" in result
        assert result["summary"] == "Test summary"
        assert len(result["chapters"]) == 1
    
    @patch('app.services.gemini.genai.GenerativeModel')
    @patch('app.services.gemini.genai.configure')
    def test_invalid_json_response(self, mock_configure, mock_model_class):
        """Test handling of invalid JSON response"""
        mock_response = MagicMock()
        mock_response.text = "This is not valid JSON"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        with pytest.raises(Exception) as exc_info:
            generate_summary_and_chapters("Test transcript", "test_api_key")
        
        assert "Failed to parse" in str(exc_info.value) or "Failed to generate" in str(exc_info.value)
    
    @patch('app.services.gemini.genai.GenerativeModel')
    @patch('app.services.gemini.genai.configure')
    def test_missing_required_fields(self, mock_configure, mock_model_class):
        """Test handling of response missing required fields"""
        mock_response = MagicMock()
        mock_response.text = json.dumps({"summary": "Test summary"})
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        with pytest.raises(Exception) as exc_info:
            generate_summary_and_chapters("Test transcript", "test_api_key")
        
        assert "missing required fields" in str(exc_info.value).lower() or "Failed to generate" in str(exc_info.value)
    
    @patch('app.services.gemini.genai.GenerativeModel')
    @patch('app.services.gemini.genai.configure')
    def test_api_error(self, mock_configure, mock_model_class):
        """Test handling of API errors"""
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_model_class.return_value = mock_model
        
        with pytest.raises(Exception) as exc_info:
            generate_summary_and_chapters("Test transcript", "test_api_key")
        
        assert "Failed to generate summary" in str(exc_info.value)
