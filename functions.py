from downloader import download_video 
import tkinter as tk 
from tkinter import filedialog
import threading
from utils import show_error,is_valid_youtube_url

def paste_url(entry_widget, root):
    """Pastes clipboard text into the given entry widget."""
    try:
        clipboard_text = root.clipboard_get().strip()
        if clipboard_text:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, clipboard_text)
        else:
            show_error("Clipboard is empty")
    except tk.TclError:  # Now correctly referenced
        show_error("Clipboard is empty or contains non-text data")

def start_download(url_entry, format_var, status_var, folder_path, progress_var,status_label,cancel_button,on_complete):
    # from utils import is_valid_youtube_url

    """######################################"""
    url = url_entry.get().strip()
    if not url or not is_valid_youtube_url(url):
        show_error("Please enter a YouTube URL")
        return
    
    folder_selected = filedialog.askdirectory()
    cancel_button.configure(state="normal")  # Enable cancel button
    
    if not folder_selected:
        return
    folder_path.set(folder_selected)

    
    def format_size_mb(bytes_value):
        """Convert size in bytes to mb"""
        if bytes_value is None:
            return ""
        return f"{bytes_value/(1024 * 1024):.2f} MB"

    def update_progress(d, progress, total_bytes):
        """ progress update logic"""
        percentage = d.get("_percent_str", "0%").strip()
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        file_size_mb = format_size_mb(total_bytes)
        
        status_var.set(f"📥{speed} | {percentage} | {file_size_mb} | {eta}")
        status_label.configure(foreground="blue")  # Optionally update the label color
        progress_var.set(progress)
        
    
    # Start download in thread 
    threading.Thread(
        target=download_video,
        args=(url, format_var.get(), folder_path.get(),),
         kwargs = {"update_progress" : update_progress, 
                   "status_var" : status_var, 
                   "progress_var" : progress_var, 
                   "cancel_button" : cancel_button, 
                   "on_complete" : on_complete
                   },
        daemon=True
    ).start()

    # Initialize UI state
    # status_label.config(foreground = "blue")
    status_var.set("Starting download...")
    progress_var.set(0)
    url_entry.delete(0, tk.END)  # Clear URL entry 