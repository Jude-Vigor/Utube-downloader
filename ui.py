import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from customtkinter import CTkImage
from PIL import Image
from functions import paste_url, start_download,truncate_text

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

def create_ui():
    root = ctk.CTk()
    root.title("")
    
    root.geometry("600x400")

    youtube_img = Image.open("youtube.ico")
    youtube_icon = CTkImage(youtube_img, size= (100,40))

    # Widgets 
    yt_label = ctk.CTkLabel(root, text="", image= youtube_icon)
    yt_label.pack(anchor="w", padx=10)

    top_frame = ctk.CTkFrame(root)
    top_frame.pack(anchor="w", fill="x", pady=5, padx=10)

    url_var = tk.StringVar()
    url_entry = ctk.CTkEntry(top_frame, textvariable=url_var, width=400)
    url_entry.pack(side="left", fill="x", expand=True)

    folder_path = tk.StringVar()

    # Load download button icon
    pause_img = Image.open("pause_icon.png")
    pause_icon = CTkImage(light_image=pause_img, dark_image=pause_img)
    paste_img = Image.open("paste_icon.png")
    paste_icon = CTkImage(light_image=paste_img, dark_image=paste_img, size=(20,20))
    download_img = Image.open("download_icon.png") 
    download_icon = CTkImage(light_image=download_img, dark_image=download_img, size=(20, 20))
    # audio_img = Image.open("audio.png").resize(100,100)
    # audio_icon = CTkImage(audio_img)

    # Download Format Selection
    format_var = tk.StringVar(value="video")  # Default format

    audio_radio = ctk.CTkRadioButton(root, text="Audio", variable=format_var, value="audio")
    audio_radio.pack(anchor="w", padx=10)

    video_radio = ctk.CTkRadioButton(root, text="Video", variable=format_var, value="video", fg_color="red")
    video_radio.pack(anchor="w", padx=10)

    download_button = ctk.CTkButton(top_frame, text="", fg_color="lightgrey", image=download_icon, height=20, width=20, command=lambda: start_download(url_entry, format_var, status_label, status_var, folder_path))
    download_button.pack(side="right")

    # Paste Button
    paste_button = ctk.CTkButton(top_frame, text="",fg_color="lightgrey", command=lambda: paste_url(url_entry, root), image = paste_icon,  height=20, width=20)
    paste_button.pack(side = "right", padx=5)

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
    progress_listbox1 = tk.Listbox(progress_tab, background="#EBEBEB")
    progress_frame = ctk.CTkFrame(progress_tab, height=90, width=570)
    progress_frame.pack(pady=0, padx=0, fill="both")
    progress_frame.pack_propagate(True)

    # Example text
    video_title = "Very Long Video Title That Keeps Extending To The Right While Downloading"
    status_text = truncate_text(f"{video_title} downloading.. In progress", 20)

    progress_vidlabel = ttk.Label(progress_frame, anchor= "w", justify= "left",text=status_text, style="progress.TLabel",wraplength=265, relief="solid")
    progress_vidlabel.pack(side="left", padx=10, pady=10)

    status_var = tk.IntVar(value=0)
    status_label = ttk.Label(progress_frame, text="0...........%", textvariable=status_var, style="progress.TLabel")
    status_label.pack(side="left")

    # Progress Bar
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    pause_button = ctk.CTkButton(progress_frame, text="", width=20, image = pause_icon, fg_color= "lightgrey", height=20)
    pause_button.pack(side="right", padx=5)
    # resume_button = ctk.CTkButton(progress_frame, text="Resume", width=80)
    # resume_button.pack(side="right", padx=5)
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
