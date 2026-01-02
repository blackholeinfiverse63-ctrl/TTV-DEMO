import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('http://localhost:5000/generate-video', { prompt });
      const { video_path } = response.data;
      const filename = video_path.split('/').pop();
      setVideoUrl(`http://localhost:5000/video/${filename}`);
    } catch (err) {
      setError('Failed to generate video');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Gurukul TTV Lesson</h1>
      <div className="input-group">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter text prompt for video generation"
          rows={4}
        />
        <button onClick={handleGenerate} disabled={loading}>
          {loading ? 'Generating...' : 'Generate Video'}
        </button>
      </div>
      {error && <p className="error">{error}</p>}
      {videoUrl && (
        <div className="video-player">
          <video controls>
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
}

export default App;