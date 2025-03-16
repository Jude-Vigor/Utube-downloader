import tkinter as tk
from tkinter import messagebox
import threading
from tkinter import filedialog, messagebox
from downloader import download_video

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
        messagebox.showwarning(title = "Clipboard Invalid", message="Clipboard is empty or does not contain text.")  # Handle empty clipboard


def browse_folder(folder_path):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)

def start_download(url_entry, format_var, status_label, status_var, folder_path):
    
    url = url_entry.get().strip() 
    format_choice = format_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter a valid YouTube URL.")
        return

    browse_folder(folder_path)  # Prompt user to select folder before download
    if not folder_path.get():
        messagebox.showwarning("Download Canceled", "No folder selected. Download was canceled.")
        return

    def update_progress_label(percentage):
        """Update progress in the main Tkinter thread using `after()`."""
        status_var.set(f"Downloading... {percentage}")  # Update the StringVar
        status_label.config(foreground="blue")  # Optionally update the label color

    # Run download in a separate thread
    download_thread = threading.Thread(
        target=download_video, 
        args=(url, format_choice, folder_path.get(), update_progress_label),  # Pass the callback here
        daemon=True
    )
    download_thread.start()

    status_var.set("Starting Download...")  # Update the StringVar
    status_label.config(foreground="blue")  # Optionally update the label color

def truncate_text(text,max_length = 30):
    return text[:max_length] + "..." if len(text) > max_length else text



