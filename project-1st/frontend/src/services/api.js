const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Process a YouTube video
 * @param {string} youtubeUrl - YouTube video URL
 * @param {string} geminiApiKey - Gemini API key
 * @returns {Promise<Object>} - Video processing result
 */
export async function processVideo(youtubeUrl, geminiApiKey) {
  const response = await fetch(`${API_BASE_URL}/api/videos/process`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      youtube_url: youtubeUrl,
      gemini_api_key: geminiApiKey,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to process video');
  }

  return response.json();
}

/**
 * Check API health
 * @returns {Promise<Object>} - Health status
 */
export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  
  if (!response.ok) {
    throw new Error('API health check failed');
  }
  
  return response.json();
}
