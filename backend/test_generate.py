from app.video_generator import generate_educational_video

prompts = ["Solar System", "Water Cycle", "Photosynthesis"]

for prompt in prompts:
    print(f"Generating video for: {prompt}")
    url = generate_educational_video(prompt)
    print(f"Generated: {url}")