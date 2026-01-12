import { useState } from 'react';

function SummaryDisplay({ result }) {
  const [copiedIndex, setCopiedIndex] = useState(null);
  const [copiedAll, setCopiedAll] = useState(false);

  const copyToClipboard = async (text, index = null) => {
    try {
      await navigator.clipboard.writeText(text);
      if (index !== null) {
        setCopiedIndex(index);
        setTimeout(() => setCopiedIndex(null), 2000);
      } else {
        setCopiedAll(true);
        setTimeout(() => setCopiedAll(false), 2000);
      }
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const formatFullOutput = () => {
    let output = `Video: ${result.video_title}\n`;
    output += `Duration: ${result.duration}\n\n`;
    output += `Summary:\n${result.summary}\n\n`;
    output += `Chapters:\n`;
    result.chapters.forEach((chapter, index) => {
      output += `\n${index + 1}. [${chapter.timestamp}] ${chapter.title}\n`;
      output += `   ${chapter.description}\n`;
    });
    return output;
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md mt-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Results</h2>
        <button
          onClick={() => copyToClipboard(formatFullOutput())}
          className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
        >
          {copiedAll ? '✓ Copied!' : 'Copy All'}
        </button>
      </div>

      <div className="mb-6">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-sm font-medium text-gray-600">Video:</span>
          <span className="text-gray-900">{result.video_title}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-gray-600">Duration:</span>
          <span className="text-gray-900">{result.duration}</span>
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-3">Summary</h3>
        <p className="text-gray-700 leading-relaxed">{result.summary}</p>
      </div>

      <div>
        <h3 className="text-xl font-semibold text-gray-800 mb-3">Chapters</h3>
        <div className="space-y-4">
          {result.chapters.map((chapter, index) => (
            <div
              key={index}
              className="p-4 bg-gray-50 rounded-lg border border-gray-200"
            >
              <div className="flex justify-between items-start mb-2">
                <div className="flex items-center gap-3">
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded">
                    {chapter.timestamp}
                  </span>
                  <h4 className="font-semibold text-gray-900">{chapter.title}</h4>
                </div>
                <button
                  onClick={() =>
                    copyToClipboard(
                      `[${chapter.timestamp}] ${chapter.title}\n${chapter.description}`,
                      index
                    )
                  }
                  className="px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors"
                >
                  {copiedIndex === index ? '✓' : 'Copy'}
                </button>
              </div>
              <p className="text-gray-600 text-sm">{chapter.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default SummaryDisplay;
