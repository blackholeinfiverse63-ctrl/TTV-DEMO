import torch
from diffusers import AnimateDiffPipeline, DDIMScheduler, MotionAdapter
from diffusers.utils import export_to_video
import os
import numpy as np
from PIL import Image, ImageFilter

def generate_video(prompt, output_path, num_frames=48, fps=24, enable_stability=True):
    """
    Generate a video from a text prompt using AnimateDiff.

    Args:
        prompt (str): Text prompt for video generation.
        output_path (str): Path to save the generated video.
        num_frames (int): Number of frames to generate (default 48 for ~2 seconds at 24fps).
        fps (int): Frames per second for the output video.

    Returns:
        str: Path to the generated video file.
    """
    # Load the motion adapter
    adapter = MotionAdapter.from_pretrained("guoyww/animatediff-motion-adapter-v1-5-2", torch_dtype=torch.float16)

    # Load SD 1.5 pipeline
    pipeline = AnimateDiffPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        motion_adapter=adapter,
        torch_dtype=torch.float16
    )
    pipeline.scheduler = DDIMScheduler.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        subfolder="scheduler",
        clip_sample=False,
        timestep_spacing="linspace",
        beta_schedule="linear",
        steps_offset=1
    )

    # Enable memory savings
    pipeline.vae.enable_slicing()

    # Move to GPU if available
    if torch.cuda.is_available():
        pipeline.to("cuda")

    # Generate video
    output = pipeline(
        prompt=prompt,
        negative_prompt="low quality, watermark",
        num_frames=num_frames,
        guidance_scale=7.5,
        num_inference_steps=25,
        generator=torch.Generator("cuda").manual_seed(42) if torch.cuda.is_available() else torch.Generator().manual_seed(42)
    )

    # Export to video
    frames = output.frames[0]
    if enable_stability:
        frames = apply_stability(frames)
    export_to_video(frames, output_path, fps=fps)

    return output_path


def apply_stability(frames):
    """
    Apply temporal stability enhancements to frames.
    Includes smoothing, tone stabilization, flicker reduction, jitter reduction.
    """
    # Convert to numpy arrays
    frame_arrays = [np.array(frame) for frame in frames]

    # 1. Flicker reduction: normalize brightness
    frame_arrays = apply_flicker_reduction_arrays(frame_arrays)

    # 2. Color correction: stabilize tone
    frame_arrays = apply_color_correction_arrays(frame_arrays)

    # 3. Temporal smoothing: smooth motion
    frame_arrays = apply_temporal_smoothing_arrays(frame_arrays)

    # 4. Jitter reduction: basic stabilization (simplified)
    frame_arrays = apply_jitter_reduction_arrays(frame_arrays)

    # Convert back to PIL
    return [Image.fromarray(f.astype(np.uint8)) for f in frame_arrays]


def apply_flicker_reduction_arrays(frame_arrays):
    """Reduce flicker by normalizing brightness."""
    grays = [np.array(Image.fromarray(f).convert('L')) for f in frame_arrays]
    means = [np.mean(g) for g in grays]
    target_mean = np.mean(means)
    corrected = []
    for f, mean in zip(frame_arrays, means):
        factor = target_mean / (mean + 1e-6)
        c = f * factor
        c = np.clip(c, 0, 255)
        corrected.append(c)
    return corrected


def apply_color_correction_arrays(frame_arrays):
    """Stabilize color tone across frames."""
    means = [np.mean(f, axis=(0,1)) for f in frame_arrays]
    target_mean = np.mean(means, axis=0)
    corrected = []
    for f, mean in zip(frame_arrays, means):
        factor = target_mean / (mean + 1e-6)
        c = f * factor
        c = np.clip(c, 0, 255)
        corrected.append(c)
    return corrected


def apply_temporal_smoothing_arrays(frame_arrays):
    """Apply temporal smoothing to reduce abrupt changes."""
    smoothed = []
    for i in range(len(frame_arrays)):
        if i == 0:
            smoothed.append(frame_arrays[i])
        elif i == len(frame_arrays)-1:
            smoothed.append(frame_arrays[i])
        else:
            # Use median for better edge preservation
            stack = np.stack([frame_arrays[i-1], frame_arrays[i], frame_arrays[i+1]])
            med = np.median(stack, axis=0)
            smoothed.append(med)
    return smoothed


def apply_jitter_reduction_arrays(frame_arrays):
    """Basic jitter reduction using Gaussian blur."""
    # Apply Gaussian blur to smooth
    smoothed = []
    for f in frame_arrays:
        img = Image.fromarray(f.astype(np.uint8))
        blurred = img.filter(ImageFilter.GaussianBlur(1))
        smoothed.append(np.array(blurred))
    return smoothed