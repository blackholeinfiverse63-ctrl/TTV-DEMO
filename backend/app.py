from flask import Flask, request, jsonify, send_from_directory
import os
from pipeline import generate_video
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Directory to save generated videos
VIDEO_DIR = "generated_videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

@app.route('/generate-video', methods=['POST'])
def generate_video_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Generate unique filename
    video_id = str(uuid.uuid4())
    output_path = os.path.join(VIDEO_DIR, f"{video_id}.mp4")

    try:
        # Generate video
        generate_video(prompt, output_path, num_frames=16, fps=24)  # ~0.7 seconds for test
        return jsonify({"video_path": output_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/video/<filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_DIR, filename, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True)