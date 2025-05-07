import customtkinter as ctk
import tkinter as tk
from tkinter import ttk,messagebox
from customtkinter import CTkImage
from PIL import Image, ImageTk, ImageSequence
from utils import truncate_text
from functions import  start_download,paste_url
from downloader import  toggle_pause_resume, stop_download,fetch_video_info,download_process,download_active
from threading import Thread
import os
from send2trash import send2trash

global pause_icon,resume_icon 


pause_icon = ctk.CTkImage(Image.open("assets/images/pause_icon2.png"), size=(20, 20))
resume_icon = ctk.CTkImage(Image.open("assets/images/resume_icon2.png"), size=(20, 20))
cancel_icon = CTkImage(Image.open("assets/images/cancel_icon2.png"), size=(20, 20))
delete_icon = CTkImage(Image.open("assets/images/delete_icon.png"), size= (20,20))
# go_to_file_icon = CTkImage(Image.open("assets/images/go_to_file.png"), size= (20,20))

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
# cancel_button = {"value":""}

downloaded_files = []  # This holds file paths of completed downloads
downloaded_frame = None  # Will hold reference to the container for each downloaded item

def on_download_complete(file_path, ):
    print("✅ Download complete:", file_path)
    cancel_button.configure(state="disabled")

    downloaded_files.append(file_path)
    downloaded_frame.after(0, refresh_downloaded_tab)

def safe_destroy(widget):
    try:
        if widget.winfo_exists():
            widget.destroy()
            widget.clear()
    except:
        pass  # Avoid crashing if already destroyed or invalid

def refresh_downloaded_tab():
    for widget in downloaded_frame.winfo_children():
        safe_destroy(widget)

    for file_path in downloaded_files:
        item_frame = ctk.CTkFrame(downloaded_frame, height=90, width=570, border_width=2)
        item_frame.pack(pady=5, padx=10, fill="x")
        item_frame.pack_propagate(False)

        file_name = os.path.basename(file_path)
        short_name = truncate_text(file_name,40)

        label = ttk.Label(item_frame, text=short_name, style="progress.TLabel")
        label.pack(side="left", padx=20)

        go_btn = ctk.CTkButton(item_frame, text="Go to file",  height=25, width=20, fg_color="blue" ,command=lambda p=file_path: os.startfile(os.path.dirname(p)))
        go_btn.pack(side="right", padx=10)

        del_btn = ctk.CTkButton(item_frame, text="",image= delete_icon, height=20, width=20, fg_color="lightgrey", command=lambda p=file_path, f=item_frame: delete_file(p, f))
        del_btn.pack(side="right", padx=5)

        play_btn = ctk.CTkButton(item_frame, text="", image= resume_icon, height=20, width=20, fg_color="lightgrey", command=lambda p=file_path: os.startfile(p))
        play_btn.pack(side="right", padx=5)


        # Add tooltip to show full filename on hover
        label.bind("<Enter>", lambda e, t=file_name: show_tooltip(e, t))
        label.bind("<Leave>", hide_tooltip)


def delete_file(path, frame_widget):
    # Ask the user for confirmation
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to move this file to Recycle Bin?\n\n{os.path.basename(path)}")
    if not confirm:
        return

    try:
        # os.remove(path)
        send2trash(path)
        downloaded_files.remove(path)
        if frame_widget.winfo_exists():
            frame_widget.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Could not delete file:\n{e}")

# ---Root and Widgets setup ---
def create_ui():
    root = ctk.CTk()
    root.title("Vigor YT Downloader")
    root.geometry("700x400")

    youtube_img = Image.open("assets/images/youtube.ico")
    youtube_icon = CTkImage(youtube_img, size= (100,40))
    global cancel_button
    # Create a global BooleanVar to manage pause/resume state
    is_paused_var = tk.BooleanVar(value=False)

    def on_toggle(btn, status_var):
        from downloader import download_active                                  # import the flag
        # global download_active
        if  not download_active :
            print(f"download_active : {download_active}")
            print(f"download_process : {download_process}")
            print("⚠️ Cannot resume: No active download.")
            
            status_var.set("⚠️ No active Download .")
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

    def on_cancel(cancel_button,status_var,progress_var,vid_title_var):
        from downloader import download_active    
        # global download_active
        response = messagebox.askyesno("Cancel Download", "Are you sure you want to cancel the download?")
        if response: # i.e if yes;
            if download_active or download_process is not None:
                stop_download()
                cancel_button.configure(state="disabled")
                status_var.set("❌ Download cancelled.")
                status_label.configure(foreground="red")
                progress_var.set(0)
                vid_title_var.set("Video title will appear here.")
                # tooltip(text = "")

                status_label.after(4000, lambda: status_var.set(""))
            else:
                pass
        else:
            pass
    # Widgets 
    yt_label = ctk.CTkLabel(root, text="", image= youtube_icon)
    yt_label.pack(anchor="w", padx=10)

    top_frame = ctk.CTkFrame(root)
    top_frame.pack(anchor="w", fill="x", pady=5, padx=10)
    
    url_var = tk.StringVar()
    url_entry = ctk.CTkEntry(top_frame, textvariable = url_var, width=400, )
    url_entry.pack(side="left", fill="x", expand=True)
    root.after(200, lambda:url_entry.focus_set())
    
    folder_path = tk.StringVar()

    last_url = {"value": ""} ## use a mutable object to allow updates inside nested function without declaring nonlocal scope

    def on_url_entry(event=None):
        from utils import is_valid_youtube_url
        url = url_entry.get().strip()
        print("URL entered:", url)  # Debug print

        if not url or not is_valid_youtube_url(url):
            vid_title_var.set("Video title will appear here.")
            return
        if url == last_url["value"]:
            pass
        
        last_url["value"] = url
        vid_title_var.set("Fetching video info...")
        spinner_label.pack(side="left", padx=5)

        def fetch_and_update(url):
            info = fetch_video_info(url)
            # print("Fetched info:", info)

            if info:
                
                title = info.get("title", "Unknown Title")
                global full_title
                full_title= title
                print(full_title) # For debug
                truncated = truncate_text(f"{full_title}", 20)

                # Update label safely from thread
                url_entry.after(0, lambda: vid_title_var.set( truncated))
                # root.after(0, lambda: root.title(full_title))  # <-- Set window title
            else:
                url_entry.after(0, lambda: vid_title_var.set("❌ Could not fetch video info."))
                
                # Always hide spinner when done
            spinner_label.after(0, spinner_label.pack_forget)

        Thread(target = fetch_and_update, args=(url,), daemon = True).start()    
    
    url_var.trace_add("write", lambda *args: on_url_entry())
    url_entry.bind("<Return>", on_url_entry)    # when user presses Enter  
    # url_entry.bind("<KeyRelease>", on_url_entry)

    # Load icons
    paste_img = Image.open("assets/images/paste_icon.png")
    paste_icon = CTkImage(light_image=paste_img, dark_image=paste_img, size=(20,20))
    download_img = Image.open("assets/images/download_icon.png") 
    download_icon = CTkImage(light_image=download_img, dark_image=download_img, size=(20, 20))

    # Download Format Selection
    format_var = tk.StringVar(value="video")  # Default format

    audio_radio = ctk.CTkRadioButton(root, text="Audio", variable=format_var, value="audio")
    audio_radio.pack(anchor="w", padx=10)
    video_radio = ctk.CTkRadioButton(root, text="Video", variable=format_var, value="video", fg_color="red")
    video_radio.pack(anchor="w", padx=10)

    download_button = ctk.CTkButton(top_frame, text="", fg_color="lightgrey", image=download_icon, height=20, width=20, 
                                    command=lambda: start_download(url_entry, format_var,  status_var, folder_path, progress_var,status_label,cancel_button, on_download_complete))
    download_button.pack(side="right")

    paste_button = ctk.CTkButton(top_frame, text="",fg_color="lightgrey", command=lambda: paste_url(url_entry, root), image = paste_icon,  height=20, width=20)
    paste_button.pack(side = "right", padx=5)

    def create_spinner(parent_frame):
        spinner_path = "assets/images/spinner.gif"  # Ensure it's animated GIF
        spinner_img = Image.open(spinner_path)
        spinner_frames = []

        try:
            while True:
                spinner_frames.append(spinner_img.copy())
                spinner_img.seek(len(spinner_frames))
        except EOFError:
            pass

        photo_images = [ImageTk.PhotoImage(frame.copy().resize((20,20), Image.LANCZOS)) for frame in spinner_frames]

        label = tk.Label(parent_frame, anchor="w", justify= "left",bd=0)
        
        def animate(index=0):
            frame = photo_images[index]
            label.configure(image=frame)
            label.image = frame
            index = (index + 1) % len(photo_images)
            label.after(100, animate, index)

        animate()
        return label

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

    # Wrap Vid_titlelabel and spinner in a frame
    title_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")  # Transparent background
    title_frame.pack(side="left", padx=10, pady=10)
    vid_title_var = tk.StringVar()
    vid_title_var.set("Video title will appear here.")
    vid_titlelabel = ttk.Label(title_frame, anchor="w", justify="left", textvariable=vid_title_var, style="progress.TLabel", wraplength=265, width=25, relief="solid")
    vid_titlelabel.pack(side="left")

    spinner_label = create_spinner(title_frame)
    spinner_label.pack(side="left", padx=5, pady=5)
    spinner_label.pack_forget()

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
                                   command= lambda: on_cancel(cancel_button, status_var, progress_var,vid_title_var, ))
    cancel_button.configure(state = "disabled")
    
    cancel_button.pack(side = "right", padx = 5 )
                       
    progress_listbox1.pack(fill="both", expand=True)


    # Create scrollable canvas inside downloaded_tab
    downloaded_scroll = tk.Canvas(downloaded_tab, bg="#EBEBEB", height=400)
    downloaded_scroll.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(downloaded_tab, orient="vertical", command=downloaded_scroll.yview)
    scrollbar.pack(side="right", fill="y")

    downloaded_scroll.configure(yscrollcommand=scrollbar.set)

    # Create the container inside the scrollable canvas
    downloaded_container = tk.Frame(downloaded_scroll, bg="#EBEBEB")
    downloaded_scroll.create_window((0, 0), window=downloaded_container, anchor="nw")

    downloaded_container.bind("<Configure>", lambda e: downloaded_scroll.configure(scrollregion=downloaded_scroll.bbox("all")))

    #  Now assign it globally
    global downloaded_frame
    downloaded_frame = downloaded_container
                                                            
    #  And finally load previous files (if folder is set)
    if folder_path.get():
        refresh_downloaded_tab()

    # def on_configure(event):
    #     downloaded_scroll.configure(scrollregion=downloaded_scroll.bbox("all"))

    # downloaded_container.bind("<Configure>", on_configure)

    progress_listbox1.pack(fill="both", expand=True)

    notebook.add(progress_tab, text="In Progress")
    notebook.add(downloaded_tab, text="Downloaded")



    root.mainloop()