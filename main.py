import argparse
import os
import subprocess
import tempfile
import shutil
import threading
from time import perf_counter
from os import system as run, path

import cv2 as cv
from pydub import AudioSegment
from pydub.playback import play
from fpstimer import FPSTimer
from concurrent.futures import ThreadPoolExecutor

import yt_dlp

if os.name == "nt":
    try:
        from win32api import SetConsoleTitle as title
    except ImportError:
        title = None


def download_youtube_video(url, download_dir):
    """
    Downloads the YouTube video (merged with best audio) as an MP4 file.
    Returns the full path to the downloaded video.
    """
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": os.path.join(download_dir, "video.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        base, _ = os.path.splitext(filename)
        video_path = base + ".mp4"
        if not path.exists(video_path):
            raise FileNotFoundError("Video file was not downloaded correctly.")
        return video_path


def extract_audio(video_path, audio_path):
    """
    Extracts the audio from the video file into an MP3 file using ffmpeg.
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-q:a",
        "0",
        "-map",
        "a",
        audio_path,
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def process_frame(frame, ascii_width, ascii_height, ascii_chars):
    """
    Converts a single frame (a numpy array) to an ASCII art string.
    """
    # Convert to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Resize the frame to desired ascii dimensions
    resized = cv.resize(gray, (ascii_width, ascii_height))
    # Build the ASCII string. Each pixel is mapped to a character.
    lines = []
    for row in resized:
        line = "".join(
            ascii_chars[
                round(max(int(pixel) / 255 * (len(ascii_chars) - 1), 0))
            ]
            for pixel in row
        )
        lines.append(line)
    # Move the cursor to the top-left before drawing the next frame
    return "\x1b[1;1H" + "\n".join(lines)


def play_video(video_path, audio_path):
    """
    Processes the video into ASCII frames, starts audio playback,
    and then prints each frame at the proper FPS.
    """
    vid = cv.VideoCapture(video_path)
    if not vid.isOpened():
        raise RuntimeError("Failed to open video file: " + video_path)

    # Get video properties
    vidWidth = int(vid.get(cv.CAP_PROP_FRAME_WIDTH))
    vidHeight = int(vid.get(cv.CAP_PROP_FRAME_HEIGHT))
    vidFrameCount = int(vid.get(cv.CAP_PROP_FRAME_COUNT))
    vidFPS = vid.get(cv.CAP_PROP_FPS)

    # ASCII conversion settings:
    ascii_width = 180
    aspect_ratio = vidWidth / vidHeight
    ascii_height = int(ascii_width / aspect_ratio * 0.55)  # adjust factor for terminal fonts
    ascii_chars = (" ", ".", "°", "*", "o", "O", "#", "@")
    ascii_frames = []

    # Clear the console (works on Windows and Unix)
    run("cls" if os.name == "nt" else "clear")

    renderStartTime = perf_counter()

    def process_frame_wrapper(frame):
        return process_frame(frame, ascii_width, ascii_height, ascii_chars)

    # Process all frames concurrently
    futures = []
    num_workers = os.cpu_count()
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        frame_idx = 0
        while True:
            ret, frame = vid.read()
            if not ret:
                break
            frame_idx += 1
            # Display progress in the terminal
            doneFrames = frame_idx
            elapsed = perf_counter() - renderStartTime
            remaining = ((elapsed / (doneFrames or 1)) * (vidFrameCount - doneFrames))
            print(
                f"Processing frame {frame_idx}/{vidFrameCount} || "
                f"{round(frame_idx / vidFrameCount * 100)}% || ETC: {remaining:.2f}s",
                end="\r",
            )
            futures.append(executor.submit(process_frame_wrapper, frame))

        # Collect processed ASCII frames
        for future in futures:
            ascii_frames.append(future.result())

    # Prepare audio playback in a separate thread.
    audio = AudioSegment.from_file(audio_path, format="mp3")

    def play_audio():
        try:
            play(audio)
        except KeyboardInterrupt:
            pass

    audio_thread = threading.Thread(target=play_audio, daemon=True)
    audio_thread.start()

    timer = FPSTimer(vidFPS)
    for index, ascii_frame in enumerate(ascii_frames, start=1):
        # On Windows, you can adjust the console window size periodically.
        if os.name == "nt" and index % 10 == 0:
            run(f"mode CON: cols={ascii_width} lines={ascii_height}")
        # Update the console title with playback progress (if available)
        remMin, remSec = divmod(index // round(vidFPS), 60)
        totMin, totSec = divmod(vidFrameCount // round(vidFPS), 60)
        title_str = f"({remMin}:{remSec:02}/{totMin}:{totSec:02}) {index}/{vidFrameCount}"
        if title is not None:
            title(title_str)
        # Print the ASCII frame
        print(ascii_frame, end="")
        timer.sleep()

    vid.release()
    if audio_thread.is_alive():
        audio_thread.join(timeout=1.0)


def main():
    parser = argparse.ArgumentParser(
        description="Play a YouTube video in the terminal as ASCII art."
    )
    parser.add_argument("url", nargs="?", help="YouTube URL of the video to play")
    args = parser.parse_args()

    if not args.url:
        args.url = input("Please enter a YouTube URL: ")

    temp_dir = tempfile.mkdtemp(prefix="asciimation_")
    try:
        print("Downloading video...")
        video_path = download_youtube_video(args.url, temp_dir)
        print("Extracting audio...")
        audio_path = os.path.join(temp_dir, "audio.mp3")
        extract_audio(video_path, audio_path)
        print("Converting video to ASCII and starting playback...")
        play_video(video_path, audio_path)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main()
