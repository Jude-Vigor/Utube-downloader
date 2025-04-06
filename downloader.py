import subprocess
import psutil
import re
from utils import is_valid_youtube_url, show_error

# Global state
download_process = None
current_progress = 0

def progress_callback(progress, message="Downloading..."):
    """Handles progress updates"""
    print(f"{message} {progress:.1f}%")  # Replace with actual UI update logic


def download_video(url, format_choice, folder_path, update_progress=None, status_var=None, progress_var=None):
    global download_process, current_progress
    
    if not is_valid_youtube_url(url):
        show_error("Invalid YouTube URL")
        return

    format_flag = "bestaudio/best" if format_choice == "audio" else "bestvideo+bestaudio"

    try:
        download_process = subprocess.Popen(
            [
                "yt-dlp", url,
                "-f", format_flag,
                "-o", f"{folder_path}/%(title)s.%(ext)s",
                "--newline", "--no-color", "--console-title"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        # Monitor Progress

        for line in download_process.stdout:
            if "[download]" in line:
                match = re.search(r'(\d+\.?\d*)%', line)
                if match:
                    current_progress = float(match.group(1))

                    dummy_data = {
                        '_percent_str': f"{current_progress}%",
                        '_speed_str': 'N/A',  # You can parse this from yt-dlp if needed
                        '_eta_str': 'N/A'
                    }

                    if update_progress:
                        update_progress(dummy_data, current_progress, None)
                elif "error" in line.lower():
                    handle_error(line.strip())
                    break

                # Handle completion
            if download_process.returncode == 0:
                if update_progress:
                    dummy_data = {
                        '_percent_str': '100%',
                        '_speed_str': 'Done',
                        '_eta_str': ''
                    }
                    update_progress(dummy_data, 100, None)
                else:
                    progress_callback(100, "Download complete!")
    except Exception as e:
        handle_error(str(e))  # ✅ This closes the try-except properly


    def handle_error(error_msg):
        show_error(error_msg)
        if update_progress:
            dummy_data = {
                '_percent_str': '0%',
                '_speed_str': 'Error',
                '_eta_str': ''
            }
            update_progress(dummy_data, 0, None)
        else:
            progress_callback(0, "Error occurred")


def toggle_pause_resume(is_paused_var):
    global download_process

    if download_process is None or download_process.poll() is not None:
        print("No active download process.")
        is_paused_var.set(False)  # Reset to 'not paused' if no process is running
        return

    if is_paused_var.get():  # If the download is paused
        resume_download()  # Resume the download
        is_paused_var.set(False)  # Update the paused state to False
        print("Download resumed successfully")
    else:  # If the download is not paused
        pause_download()  # Pause the download
        is_paused_var.set(True)  # Update the paused state to True
        print("Download paused successfully")

    print("is_paused_var is now:", is_paused_var.get())  # Debug output

def pause_download():
    global download_process
    if download_process:
        try:
            p = psutil.Process(download_process.pid)
            for child in p.children(recursive=True):
                child.suspend()
            p.suspend()
            print("Download paused successfully")
        except psutil.NoSuchProcess:
            print("Process not found (already exited?)")


def resume_download():
    global download_process
    if download_process:
        try:
            p = psutil.Process(download_process.pid)
            for child in p.children(recursive=True):
                child.resume()
            p.resume()
            print("Download resumed successfully")
        except psutil.NoSuchProcess:
            print("Process not found (already exited?)")


def stop_download():
    global download_process
    if download_process:
        try:
            p = psutil.Process(download_process.pid)
            for child in p.children(recursive=True):
                child.terminate()
            p.terminate()
            download_process = None
            print("Download stopped successfully")
        except psutil.NoSuchProcess:
            print("Process not found (already exited?)")
