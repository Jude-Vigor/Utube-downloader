import tkinter as tk
from tkinter import messagebox
import threading
from tkinter import filedialog, messagebox
from downloader import download_video
# from utils import truncate_text


def paste_url(entry_widget, root):
    """Pastes clipboard text into the given entry widget."""
    try:
        clipboard_text = root.clipboard_get()  # Get text from clipboard
        if clipboard_text.strip(): #check if clipboard has a content
            entry_widget.delete(0, tk.END)  # Clear existing content
            entry_widget.insert(0, clipboard_text)  # Insert clipboard text
        else :
            messagebox.showwarning("Clipboard Empty", "Clipboard is empty. Copy a URL first.")
    except tk.TclError:
        messagebox.showwarning(title = "Clipboard Invalid", message= "Clipboard is empty or does not contain text.")  # Handle empty clipboard


def browse_folder(folder_path):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)

def start_download(url_entry, format_var, status_label, status_var, folder_path,progress_var):
    
    url = url_entry.get().strip() 
    format_choice = format_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter a valid YouTube URL.")
        return

    browse_folder(folder_path)  # Prompt user to select folder before download
    if not folder_path.get():
        messagebox.showwarning("Download Canceled", "No folder selected. Download was canceled.")
        return
    
    url_entry.delete(0, tk.END) #clears the entry box when download starts'''



    def format_size_mb(bytes_value):
        '''convert bytes to Mb'''
        if bytes_value is None:
            return ""
        return f"{bytes_value/(1024 * 1024):.2f} MB"

    def update_progress_label(d,percentage,speed,eta,progress, total_bytes):
        """Update progress in the main Tkinter thread using `after()`."""
        file_size_mb = format_size_mb(total_bytes)
        text = f"📥{speed} | {percentage} | {file_size_mb} | {eta}"

        if d["status"] == "downloading":
            status_var.set(text)  # Update the StringVar
            status_label.config(foreground="blue")  # Optionally update the label color
            progress_var.set(progress)
        
        elif d['status'] == 'finished':
            status_var.set("Processing file...")  # Show processing stage
            progress_var.set(95)  # Set to 95% to leave room for merging

        elif d['status'] == 'error':
            error_message = d.get('error', 'An unknown error occured!') # fetches the error but if none, falls on a custom error(An unknown error)
            # Check if it's a network issue
            if "Unable to download webpage" in error_message or "getaddrinfo failed" in error_message:
                error_message = "No internet connection. Please check your network and try again."

            
            messagebox.showerror("Download error!", error_message)
            status_var.set("")
        



        

         # ✅ Move to "Downloaded" list once finished
        
        
    # Run download in a separate thread
    download_thread = threading.Thread(
        target=download_video, 
        args=(url, format_choice, folder_path.get(), update_progress_label,status_var,progress_var),  # Pass the callback here
        daemon=True
    )
    download_thread.start()

    status_var.set("Starting Download...")  # Update the StringVar
    status_label.config(foreground="blue")  # Optionally update the label color


def listbox_get_index(listbox, text):
    """Find the index of a text in a Listbox."""
    items = listbox.get(0, tk.END)
    for i, item in enumerate(items):
        if text in item:
            return i
    return None

# def pause_download(url):
#     """Pauses the download by stopping the process"""
#     if url in active_downloads:
#         active_downloads[url].pause()  # This may not work with yt-dlp
#         del active_downloads[url]  # Remove from tracking

# def resume_download(url):
#     """Resumes the download by restarting it"""
#     if url in active_downloads:
#         format = "best"  # Adjust this based on your UI
#         folder = "./downloads"  # Adjust this based on your UI
#         start_download(url, format, folder, None, None)  # Restart download