import { useState } from 'react';
import VideoInput from './components/VideoInput';
import SummaryDisplay from './components/SummaryDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import { processVideo } from './services/api';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async ({ youtubeUrl, geminiApiKey }) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await processVideo(youtubeUrl, geminiApiKey);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <VideoInput onSubmit={handleSubmit} isLoading={isLoading} />
        
        {isLoading && <LoadingSpinner />}
        
        {error && (
          <div className="w-full max-w-2xl mx-auto mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            <p className="font-medium">Error:</p>
            <p>{error}</p>
          </div>
        )}
        
        {result && <SummaryDisplay result={result} />}
      </div>
    </div>
  );
}

export default App;
