import subprocess
import psutil
import re
from utils import is_valid_youtube_url, show_error
from yt_dlp import YoutubeDL
from utils import sanitize_filename

# Global state
download_process = None
download_active = False
current_progress = 0

def progress_callback(progress, message="Downloading..."):
    """Handles progress updates"""
    print(f"{message} {progress:.1f}%")  # Replace with actual UI update logic


def fetch_video_info(url):
    print(f"Fetching info for: {url}")  

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print("Video title:", info.get("title", "N/A"))  

            return info
    except Exception as e:
        print("Error fetching video info:", e)
        return None
    

def download_video(url, format_choice, folder_path, update_progress=None, status_var=None, progress_var=None, cancel_button = None, on_complete=None):
    global download_process, current_progress, download_active
    download_active = True
    
    final_path = None

    def handle_error(error_msg):
        global download_active, download_process  # Ensure we can modify the outer scope variable
        
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
            download_active = False  # **CRITICAL: Set to False on error**
            download_process = None  # **CRITICAL: Also reset process**
    
    if not is_valid_youtube_url(url):
        show_error("Invalid YouTube URL")
        return

    format_flag = "bestaudio/best" if format_choice == "audio" else "bestvideo+bestaudio"

    try:

        video_info = fetch_video_info(url)
        is_playlist = 'entries' in video_info if video_info else False

        if is_playlist:
            output_template = f"{folder_path}/%(playlist_index)s - %(title)s.%(ext)s"
        else:
            title = video_info.get("title", "video") if video_info else "video"
            safe_title = sanitize_filename(title)
            output_template = f"{folder_path}/{safe_title}.%(ext)s"


        download_process = subprocess.Popen(
        [
                "yt-dlp",
                # '--cookies-from-browser', 'chrome',  #Automatically extract your YouTube login cookies from your Chrome browser, 
                                                    #so it can act like you are watching/downloading the video.
                "--newline", 
                "--no-color", 
                "--console-title",
                "-f", format_flag,
                "-o", output_template,
                url
        ],


            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
        # Monitor Progress/ stdout loop where you detect the downloaded file path
        for line in download_process.stdout:
            line = line.strip()
            print("YT-DLP LINE:", line)  # for debug

            # ✅ Catch audio or non-merged downloads
            if "[download]" in line and "Destination:" in line:
                match = re.search(r'Destination:\s+(.+)', line)
                if match:
                    final_path = match.group(1).strip()
                    print("✅ Audio file path detected:", final_path)
                        #  Detect merged final file

            if "[Merger]" in line and "Merging formats into" in line:
                match = re.search(r'Merging formats into\s+"(.+?)"', line)
                if match:
                    final_path = match.group(1).strip()
                    print("✅ Final merged path:", final_path)
            # Extract percentage progress
            if "[download]" in line:
                match = re.search(r'(\d+\.?\d*)%', line)
                if match:
                    current_progress = float(match.group(1))

                 # Extract size, speed, estimated time remaing
                size_match = re.search(r'of\s+([\d\.]+\w+)', line)
                speed_match = re.search(r'(\d+\.?\d*\s?[KMG]?i?B/s)', line)                
                eta_match = re.search(r'ETA (\d+:\d+)', line)

                # Assign values or fallback to 'N/A' if no value found
                total_size = size_match.group(1) if size_match else 'N/A'
                speed = speed_match.group(1) if speed_match else 'N/A'
                eta = eta_match.group(1) if eta_match else 'N/A'

                dummy_data = {
                    '_percent_str': f"{current_progress}% of {total_size}",
                    '_speed_str': speed,  # 
                    '_eta_str': eta
                }

                if update_progress:
                        update_progress(dummy_data, current_progress, None)

                elif "error" in line.lower():
                    handle_error(line.strip())
                    break
        # Exit thread early if user cancelled the download
        if not download_active:
            print("Thread exiting because download was cancelled.")
            return
        
        # ----- Handle completion after process output is done -----
        process_ref = download_process  # Save process before it might be set to None elsewhere

        if download_active and process_ref is not None:
            try:
                process_ref.wait()

                if process_ref.returncode == 0:
                    if update_progress:
                        dummy_data = {
                            '_percent_str': '100%',
                            '_speed_str': 'Done',
                            '_eta_str': '✅'
                        }
                        update_progress(dummy_data, 100, None)
                    else:
                        progress_callback(100, "Download complete!")

                    if on_complete and final_path:
                        on_complete(final_path)

                else:
                    handle_error("⚠️ Download failed or was cancelled.")
            except Exception as e:
                handle_error(f"⚠️ Error during wait: {e}")
        else:
            print("⏹️ Download was cancelled early or never started.")

    except Exception as e:
        handle_error(str(e))  # This closes the try-except properly
    finally:
        download_active = False  # **CRITICAL:  Always reset after download**
        download_process = None  # **CRITICAL:  Also reset process**


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
    global download_process, download_active
    download_active = False  # Set download_active state to false when user click cancel 

    if not download_process:
        print("No active download to cancel.")
        return

    try:
        p = psutil.Process(download_process.pid)

        # Terminate child processes first
        for child in p.children(recursive=True):
            child.terminate()

        # Then terminate the main download process
        p.terminate()
        try:
            # Wait up to 5 seconds for process to terminate
            p.wait(timeout=5)
            print("✅ Download stopped successfully.")
        except psutil.TimeoutExpired:
            print("⚠️ Process did not terminate within timeout.")
        download_process = None  # Reset the global reference

    except psutil.NoSuchProcess:
        print("⚠️ Process not found. Might have already exited.")
        download_process = None  # Clean up just in case

    except Exception as e:
        print(f"❌ Error stopping download: {e}")

    else:
        print("❗Cancel aborted by user.")