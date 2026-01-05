import numpy as np
from moviepy import ColorClip, Circle
import cv2  # for metrics

def test_temporal_stability():
    # Create a simple video with a moving circle
    duration = 5
    size = (640, 480)
    background = ColorClip(size=size, color=(0, 0, 0), duration=duration)
    circle = Circle(radius=50, color=(255, 0, 0)).set_position(lambda t: (320 + 100 * np.sin(2 * np.pi * t), 240)).set_duration(duration)
    video = background + circle

    # Extract frames
    frames = []
    for t in np.linspace(0, duration, 24 * duration):
        frame = video.get_frame(t)
        frames.append(frame)

    # Calculate position variance
    positions = []
    for frame in frames:
        # Find circle center (simple way, assume red circle)
        red_pixels = np.where(frame[:, :, 0] > 200)
        if red_pixels[0].size > 0:
            center_x = np.mean(red_pixels[1])
            center_y = np.mean(red_pixels[0])
            positions.append((center_x, center_y))

    if positions:
        pos_array = np.array(positions)
        variance = np.var(pos_array, axis=0)
        print(f"Position variance: {variance}")
        # Low variance means stable
        assert variance[0] < 10, "High jitter in x"
        assert variance[1] < 10, "High jitter in y"
    else:
        print("No positions detected")

    print("Stability test passed")

if __name__ == "__main__":
    test_temporal_stability()