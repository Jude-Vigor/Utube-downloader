import subprocess
import signal
import yt_dlp
from utils import is_valid_youtube_url, show_error


# Global variables to track download state
download_process = None
is_paused = False
current_progress = 0

def download_video(url,format_choice, folder_path, progress_callback=None, status_var=None, progress_var=None):
    """Downloads a video using yt-dlp in a subprocess for pause/resume support."""
    global download_process, current_progress

    if not is_valid_youtube_url(url):
        show_error("Invalid YouTube URL")
        return

    def progress_hook(d):
        if d["status"] == "downloading":
            downloaded_bytes = d.get("downloaded_bytes", 0)
            total_bytes = d.get("total_bytes", d.get("total_bytes_estimate", 1))
            progress = int((downloaded_bytes / total_bytes) * 100) if total_bytes > 0 else 0
            
            if status_var:
                status_var.set(f"Downloading... {progress}%")
                
            if progress_var:
                progress_var.set(progress)
            
            if progress_callback:
                progress_callback(d, progress, total_bytes)

        elif d['status'] == 'finished':
            if status_var:
                status_var.set("Processing file...")
            if progress_var:
                progress_var.set(95)

        elif d['status'] == 'error':
            error_message = d.get('error', 'Unknown error')
            show_error(error_message)
            if status_var:
                status_var.set("")
            if progress_var:
                progress_var.set(0)

    ydl_opts = {
        'no_color': True,
        "format": "bestaudio/best" if format_choice == "audio" else "bestvideo+bestaudio",
        "outtmpl": f"{folder_path}/%(title)s.%(ext)s",
        "progress_hooks": [progress_hook],
        
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if status_var:
            status_var.set("Download complete!")
        if progress_var:
            progress_var.set(100)
    except Exception as e:
        show_error(str(e))
        if status_var:
            status_var.set("")
        if progress_var:
            progress_var.set(0)