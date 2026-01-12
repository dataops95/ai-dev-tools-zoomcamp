import { useState } from 'react';

function VideoInput({ onSubmit, isLoading }) {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [geminiApiKey, setGeminiApiKey] = useState('');
  const [errors, setErrors] = useState({});

  const validateYoutubeUrl = (url) => {
    const patterns = [
      /(?:youtube\.com\/watch\?v=)([^&\s]+)/,
      /(?:youtu\.be\/)([^?\s]+)/,
      /(?:youtube\.com\/embed\/)([^?\s]+)/,
    ];
    
    return patterns.some(pattern => pattern.test(url));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const newErrors = {};
    
    if (!youtubeUrl.trim()) {
      newErrors.youtubeUrl = 'YouTube URL is required';
    } else if (!validateYoutubeUrl(youtubeUrl)) {
      newErrors.youtubeUrl = 'Please enter a valid YouTube URL';
    }
    
    if (!geminiApiKey.trim()) {
      newErrors.geminiApiKey = 'Gemini API key is required';
    }
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    setErrors({});
    onSubmit({ youtubeUrl, geminiApiKey });
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">
        YouTube Video Summarizer
      </h1>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="youtube-url" className="block text-sm font-medium text-gray-700 mb-2">
            YouTube URL
          </label>
          <input
            id="youtube-url"
            type="text"
            value={youtubeUrl}
            onChange={(e) => setYoutubeUrl(e.target.value)}
            placeholder="https://www.youtube.com/watch?v=..."
            className={`w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 ${
              errors.youtubeUrl ? 'border-red-500' : 'border-gray-300'
            }`}
            disabled={isLoading}
          />
          {errors.youtubeUrl && (
            <p className="mt-1 text-sm text-red-600">{errors.youtubeUrl}</p>
          )}
        </div>

        <div>
          <label htmlFor="gemini-api-key" className="block text-sm font-medium text-gray-700 mb-2">
            Gemini API Key
          </label>
          <input
            id="gemini-api-key"
            type="password"
            value={geminiApiKey}
            onChange={(e) => setGeminiApiKey(e.target.value)}
            placeholder="Enter your Gemini API key"
            className={`w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 ${
              errors.geminiApiKey ? 'border-red-500' : 'border-gray-300'
            }`}
            disabled={isLoading}
          />
          {errors.geminiApiKey && (
            <p className="mt-1 text-sm text-red-600">{errors.geminiApiKey}</p>
          )}
          <p className="mt-1 text-xs text-gray-500">
            Get your API key from{' '}
            <a 
              href="https://makersuite.google.com/app/apikey" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              Google AI Studio
            </a>
          </p>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className={`w-full py-3 px-4 rounded-md text-white font-medium transition-colors ${
            isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {isLoading ? 'Processing...' : 'Summarize Video'}
        </button>
      </form>
    </div>
  );
}

export default VideoInput;
