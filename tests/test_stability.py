import unittest
import numpy as np
from PIL import Image
import os
import tempfile
import imageio
from backend.pipeline import generate_video, apply_stability, apply_flicker_reduction_arrays, apply_color_correction_arrays, apply_temporal_smoothing_arrays, apply_jitter_reduction_arrays


class TestStability(unittest.TestCase):

    def setUp(self):
        # Create dummy frames for testing
        self.frames = [Image.fromarray(np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)) for _ in range(10)]

    def test_apply_flicker_reduction(self):
        frame_arrays = [np.array(f) for f in self.frames]
        reduced = apply_flicker_reduction_arrays(frame_arrays)
        self.assertEqual(len(reduced), len(frame_arrays))
        # Check brightness is more consistent
        grays = [np.array(Image.fromarray(f.astype(np.uint8)).convert('L')) for f in reduced]
        means = [np.mean(g) for g in grays]
        variance = np.var(means)
        self.assertLess(variance, 1000)  # Arbitrary threshold

    def test_apply_color_correction(self):
        frame_arrays = [np.array(f) for f in self.frames]
        corrected = apply_color_correction_arrays(frame_arrays)
        self.assertEqual(len(corrected), len(frame_arrays))
        # Check color means are closer
        means = [np.mean(f, axis=(0,1)) for f in corrected]
        variances = [np.var(m) for m in np.array(means).T]
        self.assertTrue(all(v < 500 for v in variances))

    def test_apply_temporal_smoothing(self):
        frame_arrays = [np.array(f) for f in self.frames]
        smoothed = apply_temporal_smoothing_arrays(frame_arrays)
        self.assertEqual(len(smoothed), len(frame_arrays))

    def test_apply_jitter_reduction(self):
        frame_arrays = [np.array(f) for f in self.frames]
        reduced = apply_jitter_reduction_arrays(frame_arrays)
        self.assertEqual(len(reduced), len(frame_arrays))

    def test_apply_stability(self):
        processed = apply_stability(self.frames)
        self.assertEqual(len(processed), len(self.frames))
        self.assertIsInstance(processed[0], Image.Image)

    def test_generate_video_with_stability(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_video.mp4")
            result = generate_video("a cat", output_path, num_frames=8, enable_stability=True)
            self.assertEqual(result, output_path)
            self.assertTrue(os.path.exists(output_path))

    def test_stability_metrics(self):
        # Generate before and after
        with tempfile.TemporaryDirectory() as tmpdir:
            before_path = os.path.join(tmpdir, "before.mp4")
            after_path = os.path.join(tmpdir, "after.mp4")
            generate_video("a dog", before_path, num_frames=8, enable_stability=False)
            generate_video("a dog", after_path, num_frames=8, enable_stability=True)
            # Compute metrics
            before_metrics = compute_stability_metrics(before_path)
            after_metrics = compute_stability_metrics(after_path)
            print(f"Before metrics: {before_metrics}")
            print(f"After metrics: {after_metrics}")
            # Assert improvements (e.g., lower variance after)
            self.assertLess(after_metrics['frame_diff_var'], before_metrics['frame_diff_var'])


def compute_stability_metrics(video_path):
    """Compute simple stability metrics."""
    frames = imageio.mimread(video_path)

    if len(frames) < 2:
        return {'frame_diff_var': 0, 'color_var': 0}

    # Frame difference variance
    diffs = []
    for i in range(1, len(frames)):
        diff = np.abs(frames[i].astype(np.float32) - frames[i-1].astype(np.float32))
        diffs.append(np.mean(diff))
    frame_diff_var = np.var(diffs)

    # Color consistency: variance of mean colors
    means = [np.mean(f, axis=(0,1)) for f in frames]
    color_var = np.var(means)

    return {'frame_diff_var': frame_diff_var, 'color_var': color_var}


if __name__ == '__main__':
    unittest.main()