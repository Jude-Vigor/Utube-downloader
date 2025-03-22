import yt_dlp
import re
from tkinter import messagebox
from ui import *
from utils import truncate_text

# def truncate_text(text,max_length = 30):
#     return text[:max_length] + "..." if len(text) > max_length else text

# YouTube URL Regex Pattern match
YOUTUBE_URL_PATTERN = re.compile(
    r"^(https?://)?(www\.)?"
    r"(youtube\.com/(watch\?v=|shorts/)|youtu\.be/)"
    r"([a-zA-Z0-9_-]{11})"
)


def is_valid_youtube_url(url):
    """Check if the given URL is a valid YouTube link."""
    return bool(YOUTUBE_URL_PATTERN.match(url))

def download_video(url, format_choice, folder_path, progress_callback,status_var,progress_var):
    if not is_valid_youtube_url(url):
        # raise ValueError("Invalid YouTube URL")
        messagebox.showwarning(title = "Url Error", message="Invalid YouTube URL")

    #     progress_label.config(text=f"Speed: {speed}\nPercent: {percent}\nETA: {eta}") 

    def progress_hook(d):
        """Handles download progress updates."""
        if d["status"] == "downloading":
            # Extract the percentage from the progress dictionary
            downloaded_bytes = d.get("downloaded_bytes", 0)
            total_bytes = d.get("total_bytes", d.get("total_bytes_estimate", 1))


            if total_bytes > 0:
                progress = int((downloaded_bytes / total_bytes) * 100)
                progress_var.set(progress)
                status_text = truncate_text(f"Downloading... {progress}%", 20)  # ✅ Truncate text before setting
                status_var.set(status_text)
                progress_var.set(progress)
                percentage = d.get("_percent_str", "0%").strip()  # Default to "0%" if missing
                speed = d.get('_speed_str', '0%')
                eta = d.get('_eta_str', 'N/A')


            if progress_callback:
                progress_callback(percentage,speed,eta,progress)  # Pass  to the callback

        elif d['status'] == 'finished':
            status_var.set("Processing file...")  # Show processing stage
            progress_var.set(95)  # Set close to 100%, but leave room for merging


    # Configure yt-dlp options
    ydl_opts = {
        "no_color": True,
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
        try:
            ydl.download([url])
            progress_var.set(100)
            status_var.set("Download Complete")
        except Exception as e:
            status_var.set(f"Error: {str(e)}")
            progress_var.set(0)  # Reset progress bar if download fails

    print(f"Downloaded {url} as {format_choice} to {folder_path}")