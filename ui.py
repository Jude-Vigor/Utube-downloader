import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from customtkinter import CTkImage
from PIL import Image
from utils import truncate_text


from functions import  start_download,paste_url



ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

def show_tooltip(event, text):
    """Displays a tooltip near the widget."""
    global tooltip  # Using a global variable to store tooltip window
    tooltip = tk.Toplevel()  # Create a new top-level window (tooltip)
    tooltip.wm_overrideredirect(True)  # Remove window decorations (title bar, border)
    tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")  # Position near cursor

    # Create a label inside tooltip
    label = tk.Label(tooltip, text=text, background="lightyellow", relief="solid", borderwidth=1)
    label.pack()

def hide_tooltip(event):
    """Hides the tooltip."""
    global tooltip
    if tooltip:
        tooltip.destroy()  # Destroy tooltip window
        tooltip = None  # Reset tooltip reference

def toggle_pause_resume():
    url = url_var.get().strip()

    if  toggle_var.get() == "running":
        pause_download(url)
        toggle_var.set("paused")
        toggle_button.configure(image=resume_icon)  # Set Resume Icon
    else:
        resume_download(url)
        toggle_var.set("running")
        toggle_button.configure(image=pause_icon)  # Set Pause Icon



def create_ui():
    root = ctk.CTk()
    root.title("")
    root.geometry("630x400")

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


    pause_icon = ctk.CTkImage(Image.open("pause_icon.png"), size=(20, 20))
    play_icon = ctk.CTkImage(Image.open("resume_icon.png"), size=(20, 20))

    # Load download button icon
    # pause_img = Image.open("pause_icon.png")
    # pause_icon = CTkImage(light_image=pause_img, dark_image=pause_img)
    # resume_img = Image.open("resume_icon.png")
    # resume_icon = CTkImage(light_image=resume_img, dark_image=resume_img)
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

    download_button = ctk.CTkButton(top_frame, text="", fg_color="lightgrey", image=download_icon, height=20, width=20, 
                                    command=lambda: start_download(url_entry, format_var, status_label, status_var, folder_path, progress_var))
    download_button.pack(side="right")

    # Paste Button
    paste_button = ctk.CTkButton(top_frame, text="",fg_color="lightgrey", command=lambda: paste_url(url_entry, root), image = paste_icon,  height=20, width=20)
    paste_button.pack(side = "right", padx=5)

    # Style
    style = ttk.Style()
    style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"), padding=[10, 5])
    style.configure("TNotebook", tabmargins=[10, 5, 10, 0])
    style.configure("progress.TLabel", font=("Helvetica", 10, "bold"), wraplength='', justify=tk.LEFT, padding=10)

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

    # Video Title text
    video_title = "Very Long Video Title That Keeps Extending To The Right While Downloading"
    title_text = truncate_text(f"{video_title} downloading.. In progress", 20)

    title_vidlabel = ttk.Label(progress_frame, anchor= "w", justify= "left",text=title_text, style="progress.TLabel",wraplength=265, relief="solid")
    title_vidlabel.pack(side="left", padx=10, pady=10)

    # Bind tooltip events
    title_vidlabel.bind("<Enter>", lambda event: show_tooltip(event, video_title))
    title_vidlabel.bind("<Leave>", hide_tooltip)

    # tooltip = None  # Initialize tooltip

    # status_var = tk.StringVar(value=truncate_text("0%", 20))  # ✅ Truncate the default text
    status_var = tk.StringVar(value="0%")  # ✅ Truncate the default text

    status_label = ttk.Label(progress_frame, text="", textvariable=status_var, style="progress.TLabel", width=40 )
    status_label.pack(side="left", )

    # Progress Bar
    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=200, mode="determinate", variable = progress_var)
    progress_bar.pack(side = "left", padx=10)

    toggle_var = ctk.StringVar(value="running")
    toggle_button = ctk.CTkButton(progress_frame, text="", textvariable= toggle_var, image = pause_icon, fg_color= "lightgrey",  )
    # command=toggle_pause_resume
    toggle_button.pack(side="right", padx=5)
    
      # Initialize tooltip

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
