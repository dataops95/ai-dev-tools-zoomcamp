import re
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


def extract_video_id(youtube_url: str) -> str:
    """
    Extract video ID from various YouTube URL formats
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/watch?v=VIDEO_ID&feature=...
    """
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([^&\s]+)',
        r'(?:youtu\.be\/)([^?\s]+)',
        r'(?:youtube\.com\/embed\/)([^?\s]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    
    raise ValueError(f"Could not extract video ID from URL: {youtube_url}")


def get_video_transcript(video_id: str) -> str:
    """
    Fetch transcript for a YouTube video
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Full transcript as a single string
        
    Raises:
        Exception: If transcript is not available
    """
    try:
        logger.info(f"Fetching transcript for video ID: {video_id}")
        
        # Get transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all text segments
        transcript_text = " ".join([item['text'] for item in transcript_list])
        
        logger.info(f"Successfully fetched transcript ({len(transcript_text)} chars)")
        return transcript_text
        
    except Exception as e:
        logger.error(f"Failed to fetch transcript: {str(e)}")
        raise Exception(
            f"Could not retrieve transcript for this video. "
            f"The video may not have captions available or may be private. "
            f"Error: {str(e)}"
        )


def get_transcript_with_timestamps(video_id: str) -> List[Dict]:
    """
    Fetch transcript with timestamps for a YouTube video
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        List of transcript segments with timestamps
    """
    try:
        logger.info(f"Fetching transcript with timestamps for video ID: {video_id}")
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        logger.info(f"Successfully fetched {len(transcript_list)} transcript segments")
        return transcript_list
    except Exception as e:
        logger.error(f"Failed to fetch transcript with timestamps: {str(e)}")
        raise
