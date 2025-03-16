import yt_dlp
import re
from tkinter import messagebox

# YouTube URL Regex Pattern match
YOUTUBE_URL_PATTERN = re.compile(
    r"^(https?://)?(www\.)?"
    r"(youtube\.com/(watch\?v=|shorts/)|youtu\.be/)"
    r"([a-zA-Z0-9_-]{11})"
)

def is_valid_youtube_url(url):
    """Check if the given URL is a valid YouTube link."""
    return bool(YOUTUBE_URL_PATTERN.match(url))

def download_video(url, format_choice, folder_path, progress_callback):
    """
    Downloads a YouTube video or audio based on the provided URL and format choice.
    
    Args:
        url (str): The YouTube video URL.
        format_choice (str): The format to download ("audio" or "video").
        folder_path (str): The folder path where the file will be saved.
        progress_callback (function): A callback function to update progress.
    """
    if not is_valid_youtube_url(url):
        # raise ValueError("Invalid YouTube URL")
        messagebox.showwarning(title = "Url Error", message="Invalid YouTube URL")
    def progress_hook(d):
        """Handles download progress updates."""
        if d["status"] == "downloading":
            # Extract the percentage from the progress dictionary
            percentage = d.get("_percent_str", "0%").strip()  # Default to "0%" if missing
            if progress_callback:
                progress_callback(percentage)  # Pass percentage to the callback

    # Configure yt-dlp options
    ydl_opts = {
        "format": "bestaudio/best" if format_choice == "audio" else "bestvideo+bestaudio",
        "progress_hooks": [progress_hook],  # Attach progress hook
        "outtmpl": f"{folder_path}/%(title)s.%(ext)s",  # Output file template
        "merge_output_format": "mp4",  # Ensure proper merging
        "postprocessors": [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
        ],
    }

    # Download the video using yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"Downloaded {url} as {format_choice} to {folder_path}")