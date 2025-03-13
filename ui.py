import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from downloader import download_video
import threading
from customtkinter import CTkImage
from PIL import Image, ImageTk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

def browse_folder(folder_path):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)

def start_download(url_entry, format_var, status_label, status_var, folder_path):
    url = url_entry.get().strip()  # Strip whitespace
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

def create_ui():
    root = ctk.CTk()
    root.title("Youtube Downloader")
    root.geometry("600x400")
    
    # Widgets 
    yt_label = ctk.CTkLabel(root, text="Youtube URL")
    yt_label.pack(anchor="w", padx=10)

    top_frame = ctk.CTkFrame(root)
    top_frame.pack(anchor="w", fill="x", pady=5, padx=10)

    url_var = tk.StringVar()
    url_entry = ctk.CTkEntry(top_frame, textvariable=url_var, width=400)
    url_entry.pack(side="left", fill="x", expand=True)

    folder_path = tk.StringVar()

    # Load download button icon
    download_img = Image.open("download_icon.png").resize((100, 100))  
    icon = CTkImage(light_image=download_img, dark_image=download_img)
    # audio_img = Image.open("audio.png").resize(100,100)
    # audio_icon = CTkImage(audio_img)

    # Download Format Selection
    format_var = tk.StringVar(value="video")  # Default format

    audio_radio = ctk.CTkRadioButton(root, text="Audio", variable=format_var, value="audio")
    audio_radio.pack(anchor="w", padx=10)

    video_radio = ctk.CTkRadioButton(root, text="Video", variable=format_var, value="video", fg_color="red")
    video_radio.pack(anchor="w", padx=10)

    download_button = ctk.CTkButton(top_frame, text="Download", image=icon, command=lambda: start_download(url_entry, format_var, status_label, status_var, folder_path))
    download_button.pack(side="left", padx=5)

    # Style
    style = ttk.Style()
    style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"), padding=[10, 5])
    style.configure("TNotebook", tabmargins=[10, 5, 10, 0])
    style.configure("progress.TLabel", font=("Helvetica", 12, "bold"), wraplength=300, justify=tk.LEFT, padding=10)

    # Notebook for Progress & Downloaded Tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", padx=10, pady=5, expand=True)

    progress_tab = ctk.CTkFrame(notebook)
    downloaded_tab = ctk.CTkFrame(notebook)

    # Progress Listbox
    progress_listbox1 = tk.Listbox(progress_tab, background="gray")
    progress_frame = ctk.CTkFrame(progress_tab, height=90, width=570)
    progress_frame.pack(pady=0, padx=0, fill="both")
    progress_frame.pack_propagate(True)

    # Example text
    video_title = "Very Long Video Title That Keeps Extending To The Right While Downloading"
    status_text = truncate_text(f"{video_title} downloading.. In progress", 20)

    progress_vidlabel = ttk.Label(progress_frame, anchor= "w", justify= "left",text=status_text, style="progress.TLabel",wraplength=265, relief="solid")
    progress_vidlabel.pack(side="left", padx=10, pady=10,)

    status_var = tk.IntVar(value=0)
    # status_label = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate")
    status_label = ttk.Label(progress_frame, text="0%", textvariable=status_var, style="progress.TLabel")
    status_label.pack(side="left")

    pause_button = ctk.CTkButton(progress_frame, text="Pause", width=80)
    pause_button.pack(side="right", padx=5)
    resume_button = ctk.CTkButton(progress_frame, text="Resume", width=80)
    resume_button.pack(side="right", padx=5)
    progress_listbox1.pack(fill="both", expand=True)

    # Downloaded Listbox
    downloaded_listbox = tk.Listbox(downloaded_tab, background="orange")
    downloaded_listbox.pack(fill="both", expand=True)

    downloaded_frame = ctk.CTkFrame(downloaded_listbox, height=90, width=570, border_width=2)
    downloaded_frame.pack(pady=10, padx=5, fill="both")
    downloaded_frame.pack_propagate(False)

    downloaded_vidlabel = ttk.Label(downloaded_frame, text="Video Title downloaded", style="progress.TLabel")
    downloaded_vidlabel.pack(side="left", padx=20)

    delete_button = ctk.CTkButton(downloaded_frame, text="Delete", width=80)
    delete_button.pack(side="right", padx=5)
    play_button = ctk.CTkButton(downloaded_frame, text="Play", width=80)
    play_button.pack(side="right", padx=5)
    go_to_button = ctk.CTkButton(downloaded_frame, text="Go to file", width=80)
    go_to_button.pack(side="right", padx=5)
    progress_listbox1.pack(fill="both", expand=True)

    notebook.add(progress_tab, text="In Progress")
    notebook.add(downloaded_tab, text="Downloaded")

    root.mainloop()
