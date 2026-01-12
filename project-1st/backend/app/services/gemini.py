import google.generativeai as genai
import json
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


def generate_summary_and_chapters(transcript: str, api_key: str) -> Dict:
    """
    Generate summary and chapter breakdown using Google Gemini API
    
    Args:
        transcript: Full video transcript text
        api_key: Gemini API key
        
    Returns:
        Dictionary with 'summary' and 'chapters' keys
        
    Raises:
        Exception: If API call fails or response is invalid
    """
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Use Gemini Pro model
        model = genai.GenerativeModel('gemini-pro')
        
        # Create prompt
        prompt = f"""Analyze this YouTube video transcript and provide:
1. A concise summary (3-5 sentences)
2. Simple chapter breakdown with timestamps in format HH:MM:SS, titles, and brief descriptions

Format the response as JSON:
{{
  "summary": "...",
  "chapters": [
    {{"timestamp": "00:00:00", "title": "...", "description": "..."}},
    ...
  ]
}}

Transcript: {transcript}
"""
        
        logger.info("Generating summary and chapters with Gemini API")
        
        # Generate content
        response = model.generate_content(prompt)
        
        logger.info("Received response from Gemini API")
        
        # Extract text from response
        response_text = response.text
        
        # Try to parse JSON from response
        # Sometimes the response may include markdown code blocks
        json_text = response_text
        if "```json" in response_text:
            # Extract JSON from markdown code block
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_text = response_text[start:end].strip()
        elif "```" in response_text:
            # Extract from generic code block
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_text = response_text[start:end].strip()
        
        # Parse JSON
        result = json.loads(json_text)
        
        # Validate structure
        if "summary" not in result or "chapters" not in result:
            raise ValueError("Response missing required fields (summary or chapters)")
        
        if not isinstance(result["chapters"], list):
            raise ValueError("Chapters must be a list")
        
        logger.info(f"Successfully generated summary and {len(result['chapters'])} chapters")
        
        return result
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {str(e)}")
        logger.error(f"Response text: {response_text[:500]}")
        raise Exception(f"Failed to parse AI response as JSON: {str(e)}")
    
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        raise Exception(f"Failed to generate summary: {str(e)}")
