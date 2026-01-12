from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
import logging

from app.services.transcript import extract_video_id, get_video_transcript
from app.services.gemini import generate_summary_and_chapters

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/videos", tags=["videos"])


class VideoProcessRequest(BaseModel):
    """Request model for video processing"""
    youtube_url: str = Field(..., description="YouTube video URL")
    gemini_api_key: str = Field(..., description="Gemini API key")


class Chapter(BaseModel):
    """Chapter model"""
    timestamp: str = Field(..., description="Chapter timestamp (HH:MM:SS)")
    title: str = Field(..., description="Chapter title")
    description: str = Field(..., description="Chapter description")


class VideoProcessResponse(BaseModel):
    """Response model for video processing"""
    video_title: str = Field(..., description="Video title")
    duration: str = Field(..., description="Video duration")
    summary: str = Field(..., description="Video summary")
    chapters: List[Chapter] = Field(..., description="Chapter breakdown")


@router.post("/process", response_model=VideoProcessResponse)
async def process_video(request: VideoProcessRequest):
    """
    Process a YouTube video: extract transcript and generate summary with chapters
    
    Args:
        request: Video processing request with YouTube URL and Gemini API key
        
    Returns:
        Video summary and chapter breakdown
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info(f"Processing video URL: {request.youtube_url}")
        
        # Extract video ID
        try:
            video_id = extract_video_id(request.youtube_url)
        except ValueError as e:
            logger.warning(f"Invalid YouTube URL: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail="Invalid YouTube URL. Please provide a valid YouTube video URL."
            )
        
        # Get transcript
        try:
            transcript = get_video_transcript(video_id)
        except Exception as e:
            logger.error(f"Transcript extraction failed: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        
        # Generate summary and chapters using Gemini
        try:
            result = generate_summary_and_chapters(transcript, request.gemini_api_key)
        except Exception as e:
            logger.error(f"Summary generation failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate summary: {str(e)}"
            )
        
        # Prepare response
        # For MVP, we'll use simple values for video_title and duration
        # These could be enhanced in future versions using YouTube Data API
        response = VideoProcessResponse(
            video_title=f"Video {video_id}",
            duration="N/A",
            summary=result["summary"],
            chapters=[Chapter(**chapter) for chapter in result["chapters"]]
        )
        
        logger.info("Video processing completed successfully")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during video processing: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
