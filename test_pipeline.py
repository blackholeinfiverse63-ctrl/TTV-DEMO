from backend.pipeline import generate_video
import os

# Test the pipeline
prompt = 'A cat playing in a garden'
output_path = 'test_video.mp4'

try:
    result = generate_video(prompt, output_path, num_frames=2, fps=24)
    print('Video generated successfully:', result)
    print('File exists:', os.path.exists(output_path))
except Exception as e:
    print('Error:', str(e))
    import traceback
    traceback.print_exc()