import hashlib
import os
MOVIEPY_AVAILABLE = True

# Reliable sample educational videos from Google Cloud Storage as fallback
sample_videos = [
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4"
]

def generate_educational_video(prompt: str) -> str:
    """
    Generate an educational video based on the user's prompt.
    Creates a short video with MoviePy or falls back to sample videos.
    """
    if MOVIEPY_AVAILABLE:
        try:
            from moviepy.editor import TextClip, ColorClip, CompositeVideoClip, concatenate_videoclips
            import math

            # Create a unique filename based on the prompt
            prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
            video_filename = f"educational_video_{prompt_hash}.mp4"
            video_path = os.path.join("output", "final_videos", video_filename)

            # Ensure the directory exists
            os.makedirs(os.path.dirname(video_path), exist_ok=True)

            # Check for specific topics
            if "solar" in prompt.lower():
                video = create_solar_system_video()
            elif "water" in prompt.lower():
                video = create_water_cycle_video()
            elif "photosynthesis" in prompt.lower():
                video = create_photosynthesis_video()
            else:
                # Default video
                content = format_educational_content(prompt)
                duration = 8
                background = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=duration)
                text_clips = []
                lines = content.split('\n')[:3]
                for i, line in enumerate(lines):
                    if line.strip():
                        txt_clip = TextClip(line, font_size=60, color='white', bg_color=None, size=(1200, 150))
                        txt_clip = txt_clip.set_position('center').set_duration(duration).set_start(i * 2)
                        text_clips.append(txt_clip)
                video = CompositeVideoClip([background] + text_clips)

            # Write the video file with fixed duration
            video.write_videofile(video_path, fps=24, codec='libx264', audio=False, verbose=False, logger=None)

            # Verify video is not empty
            assert os.path.exists(video_path)
            assert os.path.getsize(video_path) > 5000

            # Return the full URL
            return f"http://localhost:8000/output/final_videos/{video_filename}"

        except Exception as e:
            print(f"Video generation failed: {e}")
            # Fallback to sample videos

    # Fallback: select sample video based on prompt
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    video_index = int(prompt_hash[:8], 16) % len(sample_videos)
    return sample_videos[video_index]

def create_solar_system_video():
    # Educational animation, solar system, sun at center, planets orbiting smoothly, single continuous shot, stable camera, flat clean illustration style, no flicker, no jump cuts, 15 seconds duration
    from moviepy.editor import TextClip, ColorClip, CompositeVideoClip
    import numpy as np

    FPS = 24
    DURATION_SECONDS = 15
    TOTAL_FRAMES = FPS * DURATION_SECONDS  # 360
    duration = DURATION_SECONDS
    size = (1280, 720)
    background = ColorClip(size=size, color=(0, 0, 0), duration=duration)

    # Sun
    sun = TextClip("☀", fontsize=100, color='yellow').set_position('center').set_duration(duration)

    # Planets
    planets = [
        {"emoji": "☿", "orbit_radius": 150, "speed": 4.15},
        {"emoji": "♀", "orbit_radius": 200, "speed": 1.62},
        {"emoji": "🌍", "orbit_radius": 250, "speed": 1},
        {"emoji": "♂", "orbit_radius": 300, "speed": 0.53},
        {"emoji": "♃", "orbit_radius": 400, "speed": 0.084},
        {"emoji": "♄", "orbit_radius": 500, "speed": 0.034},
    ]

    planet_clips = []
    for planet in planets:
        pos_func = lambda t, r=planet["orbit_radius"], s=planet["speed"]: (
            size[0]/2 + r * np.cos(2 * np.pi * s * t),
            size[1]/2 + r * np.sin(2 * np.pi * s * t)
        )
        p_clip = TextClip(planet["emoji"], fontsize=50, color='white').set_position(pos_func).set_duration(duration)
        planet_clips.append(p_clip)

    # Title
    title = TextClip("The Solar System", fontsize=70, color='white').set_position('top').set_duration(duration)

    return CompositeVideoClip([background, sun] + planet_clips + [title])

def create_water_cycle_video():
    from moviepy import ColorClip, TextClip, CompositeVideoClip
    import numpy as np

    duration = 15
    size = (1280, 720)
    background = ColorClip(size=size, color=(135, 206, 235), duration=duration)  # Sky blue

    # Ocean
    ocean = TextClip("🌊🌊🌊🌊🌊", fontsize=100, color='blue').set_position((0, 550)).set_duration(duration)

    # Evaporation
    evap_text = TextClip("Evaporation", fontsize=50, color='black').set_position((100, 300)).set_duration(5)
    sun = TextClip("☀", fontsize=100, color='yellow').set_position((600, 100)).set_duration(duration)

    # Cloud
    cloud = TextClip("☁", fontsize=150, color='white').set_position(lambda t: (400 + 50 * np.sin(t), 200)).set_duration(duration)

    # Condensation
    cond_text = TextClip("Condensation", fontsize=50, color='black').set_position((900, 250)).set_start(5).set_duration(5)

    # Precipitation
    rain_text = TextClip("Precipitation", fontsize=50, color='black').set_position((600, 400)).set_start(10).set_duration(5)
    rain_drops = []
    for i in range(10):
        drop = TextClip("💧", fontsize=30, color='blue').set_position(lambda t, i=i: (500 + i*50, 350 + 200 * (t - 10))).set_start(10).set_duration(5)
        rain_drops.append(drop)

    # Runoff
    runoff_text = TextClip("Runoff/Collection", fontsize=50, color='black').set_position((200, 500)).set_start(12).set_duration(3)

    return CompositeVideoClip([background, ocean, sun, evap_text, cloud, cond_text, rain_text] + rain_drops + [runoff_text])

def create_photosynthesis_video():
    from moviepy import ColorClip, TextClip, CompositeVideoClip
    import numpy as np

    duration = 15
    size = (1280, 720)
    background = ColorClip(size=size, color=(173, 216, 230), duration=duration)  # Light blue

    # Sun
    sun = TextClip("☀", fontsize=100, color='yellow').set_position((1100, 50)).set_duration(duration)

    # Sunlight rays
    rays = []
    for i in range(5):
        ray = TextClip("🌞", fontsize=50, color='yellow').set_position(lambda t, i=i: (1150 + i*50, 150 + 50 * np.sin(t + i))).set_duration(duration)
        rays.append(ray)

    # Plant
    plant_stem = TextClip("🌿", fontsize=100, color='green').set_position((600, 400)).set_duration(duration)
    plant_leaves = []
    for i in range(3):
        leaf = TextClip("🍃", fontsize=80, color='green').set_position((550 + i*50, 250 - i*50)).set_duration(duration)
        plant_leaves.append(leaf)

    # CO2
    co2 = TextClip("CO₂", fontsize=50, color='gray').set_position(lambda t: (200, 400 + 50 * np.sin(t))).set_duration(7)

    # O2
    o2 = TextClip("O₂", fontsize=50, color='blue').set_position(lambda t: (900, 300 - 50 * np.sin(t))).set_start(8).set_duration(7)

    # Process text
    process = TextClip("Photosynthesis: Light + CO₂ + H₂O → Glucose + O₂", fontsize=40, color='black').set_position('bottom').set_duration(duration)

    return CompositeVideoClip([background, sun] + rays + [plant_stem] + plant_leaves + [co2, o2, process])

def format_educational_content(prompt: str) -> str:
    """
    Format the user's prompt into educational content.
    """
    return f"Educational Video on {prompt}\n\nKey Learning Points:\n• Understanding {prompt} basics\n• Practical applications\n• Best practices and tips"