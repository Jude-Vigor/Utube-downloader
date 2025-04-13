import customtkinter as ctk
import tkinter as tk
from tkinter import ttk,messagebox
from customtkinter import CTkImage
from PIL import Image
from utils import truncate_text
from functions import  start_download,paste_url
from downloader import  toggle_pause_resume, stop_download,fetch_video_info
from threading import Thread

global pause_icon,resume_icon 

pause_icon = ctk.CTkImage(Image.open("pause_icon2.png"), size=(20, 20))
resume_icon = ctk.CTkImage(Image.open("resume_icon2.png"), size=(20, 20))
cancel_icon = CTkImage(Image.open("cancel_icon2.png"), size=(20, 20))

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

def hide_tooltip(event=None):
    """Hides the tooltip."""
    global tooltip
    if tooltip:
        tooltip.destroy()  # Destroy tooltip window
        tooltip = None  # Reset tooltip reference

full_title = ''
tooltip = None


def create_ui():
    root = ctk.CTk()
    root.title("Vigor YT Downloader")
    root.geometry("700x400")

    youtube_img = Image.open("youtube.ico")
    youtube_icon = CTkImage(youtube_img, size= (100,40))

    # Create a global BooleanVar to manage pause/resume state
    is_paused_var = tk.BooleanVar(value=False)

    def on_toggle(btn, status_var):

        from downloader import download_active  # import the flag

        if not download_active:
            print("⚠️ Cannot resume: No active download.")
            status_var.set("⚠️ Cannot resume. Download cancelled.")
            return
        toggle_pause_resume(is_paused_var)

        if is_paused_var.get():  # if paused
            print("Switching to RESUME icon")
            btn.configure(image=resume_icon)
            btn.image = resume_icon
            status_var.set("⏸️ Paused...")
        else:
            print("Switching to PAUSE icon")
            btn.configure(image=pause_icon)
            btn.image = pause_icon
            status_var.set("▶️ Resuming...")

    def on_cancel(cancel_button,status_var,progress_var):

        response = messagebox.askyesno("Cancel Download", "Are you sure you want to cancel the download?")

        if response:
            stop_download()
        
            # cancel_button.configure(state="disabled")
            status_var.set("❌ Download cancelled.")
            status_label.configure(foreground="red")
            progress_var.set(0)
        else:
            pass
    # Widgets 
    yt_label = ctk.CTkLabel(root, text="", image= youtube_icon)
    yt_label.pack(anchor="w", padx=10)

    top_frame = ctk.CTkFrame(root)
    top_frame.pack(anchor="w", fill="x", pady=5, padx=10)
    
    url_var = tk.StringVar()
    url_entry = ctk.CTkEntry(top_frame, textvariable = url_var, width=400)
    url_entry.pack(side="left", fill="x", expand=True)

    folder_path = tk.StringVar()

    last_url = {"value": ""} ## use a mutable object to allow updates inside nested function without declaring nonlocal scope
    
    def on_url_entry_change(event=None):

        url = url_entry.get()
        print("URL entered:", url)  # Debug print

        if not url.strip():
            vid_title_var.set("Video title will appear here.")
            return
        if url == last_url["value"]:
            return
        
        last_url["value"] = url
        vid_title_var.set("Fetching video info...")

        def fetch_and_update(url):
            info = fetch_video_info(url)
            # print("Fetched info:", info)

            if info:
                
                title = info.get("title", "Unknown Title")
                global full_title
                full_title= title
                print(full_title) # For debug
                truncated = truncate_text(f"{full_title}", 20)

                url_entry.after(0, lambda: vid_title_var.set( truncated))
                # root.after(0, lambda: root.title(full_title))  # <-- Set window title here

            else:
                url_entry.after(0, lambda: vid_title_var.set("❌ Could not fetch video info."))

        Thread(target = fetch_and_update, args=(url,), daemon = True).start()    
    
    url_entry.bind("<FocusOut>", on_url_entry_change)  # when the user leaves the field
    url_entry.bind("<Return>", on_url_entry_change)    # when user presses Enter   

    # Load download button icon
    paste_img = Image.open("paste_icon.png")
    paste_icon = CTkImage(light_image=paste_img, dark_image=paste_img, size=(20,20))
    download_img = Image.open("download_icon.png") 
    download_icon = CTkImage(light_image=download_img, dark_image=download_img, size=(20, 20))

    # Download Format Selection
    format_var = tk.StringVar(value="video")  # Default format

    audio_radio = ctk.CTkRadioButton(root, text="Audio", variable=format_var, value="audio")
    audio_radio.pack(anchor="w", padx=10)

    video_radio = ctk.CTkRadioButton(root, text="Video", variable=format_var, value="video", fg_color="red")
    video_radio.pack(anchor="w", padx=10)

    download_button = ctk.CTkButton(top_frame, text="", fg_color="lightgrey", image=download_icon, height=20, width=20, 
                                    command=lambda: start_download(url_entry, format_var,  status_var, folder_path, progress_var,status_label))
    download_button.pack(side="right")

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
    progress_frame.pack_propagate(True) #The geometry of the slave determine the parent size

    vid_title_var = tk.StringVar()
    vid_title_var.set("Video title will appear here.")
    vid_titlelabel = ttk.Label(progress_frame, anchor= "w", justify= "left",textvariable = vid_title_var, style="progress.TLabel",wraplength=265, relief="solid")
    vid_titlelabel.pack(side="left", padx=10, pady=10)

    # Bind tooltip events
    
    vid_titlelabel.bind("<Enter>", lambda event: show_tooltip(event, full_title))
    vid_titlelabel.bind("<Leave>", hide_tooltip)

    # tooltip = None  # Initialize tooltip

    status_var = tk.StringVar(value="0%")  
    status_label = ttk.Label(progress_frame, text="", textvariable=status_var, style="progress.TLabel", width=40 )
    status_label.pack(side="left", )

    # Progress Bar
    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=200, mode="determinate", variable = progress_var)
    progress_bar.pack(side = "left", padx=10)

    # toggle_var = ctk.StringVar(value="running")
    toggle_button = ctk.CTkButton(progress_frame, text="", image = pause_icon, fg_color= "lightgrey", height=20, width=20,
                                  command=lambda: on_toggle(toggle_button,status_var ))
    toggle_button.Image = pause_icon #keep ref
    toggle_button.pack(side="right", padx=5)

    cancel_button = ctk.CTkButton(progress_frame, text= "", image = cancel_icon, fg_color= "lightgrey", height=20, width=20,
                                   command= lambda: on_cancel(cancel_button, status_var, progress_var))
    cancel_button.pack(side = "right", padx = 5 )
                       
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
