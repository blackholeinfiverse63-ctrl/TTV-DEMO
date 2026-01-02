from backend.pipeline import generate_video
import os

# Pick one prompt from Day 1
prompt = "An educational animation of the solar system: the sun at the center, planets Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune orbiting smoothly around it in their elliptical paths, with stable camera tracking following the motion, no looping artifacts, smooth transitions."

# Generate before (without stability)
print("Generating before video...")
before_path = 'output/comparison/before_solar_system.mp4'
os.makedirs('output/comparison', exist_ok=True)
generate_video(prompt, before_path, num_frames=48, fps=24, enable_stability=False)

# Generate after (with stability)
print("Generating after video...")
after_path = 'output/comparison/after_solar_system.mp4'
generate_video(prompt, after_path, num_frames=48, fps=24, enable_stability=True)

print("Comparison videos generated.")
print(f"Before: {before_path}")
print(f"After: {after_path}")

# Compute metrics
from tests.test_stability import compute_stability_metrics

before_metrics = compute_stability_metrics(before_path)
after_metrics = compute_stability_metrics(after_path)

print("Before metrics:", before_metrics)
print("After metrics:", after_metrics)