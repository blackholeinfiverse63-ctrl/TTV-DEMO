import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const lessons = {
    solar_system: "An educational animation of the solar system: the sun at the center, planets Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune orbiting smoothly around it in their elliptical paths, with stable camera tracking following the motion, no looping artifacts, smooth transitions.",
    water_cycle: "An educational animation of the water cycle: water evaporating from oceans into vapor, condensing into clouds, precipitating as rain or snow back to earth, flowing into rivers and back to oceans, with smooth continuous motion and stable subject tracking.",
    photosynthesis: "An educational animation of photosynthesis in a plant: sunlight energy absorbed by chlorophyll in leaves, water from roots and carbon dioxide from air combined to produce glucose and oxygen, with smooth motion showing the process step by step, stable tracking."
  };

  const handleGenerate = async (lessonPrompt = null) => {
    const finalPrompt = lessonPrompt || prompt;
    if (!finalPrompt.trim()) {
      setError('Please enter a prompt or select a lesson');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('http://localhost:5000/generate-video', { prompt: finalPrompt });
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
      <div className="lessons">
        <h2>Select a Lesson:</h2>
        {Object.entries(lessons).map(([key, lessonPrompt]) => (
          <button key={key} onClick={() => handleGenerate(lessonPrompt)} disabled={loading}>
            {key.replace('_', ' ').toUpperCase()}
          </button>
        ))}
      </div>
      <div className="input-group">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Or enter custom text prompt for video generation"
          rows={4}
        />
        <button onClick={() => handleGenerate()} disabled={loading}>
          {loading ? 'Generating...' : 'Generate Custom Video'}
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