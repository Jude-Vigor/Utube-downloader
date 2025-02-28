import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from customtkinter import CTkFont
from tqdm import tqdm
import time


ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


root = ctk.CTk()
root.title("Youtube Downloader")
root.geometry("600x400")

yt_label = ctk.CTkLabel(root, text = "Youtube URL")
yt_label.pack(anchor = "w", padx = 10 )

top_frame = ctk.CTkFrame(root)
top_frame.pack(anchor = "w", fill = "x", pady = 5, padx = 10 )

url_entry = ctk.CTkEntry(top_frame, width = 400 )
url_entry.pack(side = "left", fill = "x", expand = True)

download_button = ctk.CTkButton(top_frame, text = "Download")
download_button.pack(side = "left", padx = 5)



style = ttk.Style()
style.configure("TNotebook.Tab", font=("Helvetica", 16, "bold"), padding = [10, 5])  # Style Notebook tab font 
style.configure("TNotebook", tabmargins=[10, 5, 10, 0])  # [left, top, right, bottom] margins around tabs
style.configure("progress.TLabel", font = ("Helvetica", 14, "bold"), wraplength = 300, justify = tk.LEFT, padding = 10)

# Create the notebook widget
notebook = ttk.Notebook(root)
notebook.pack(fill = "both", padx = 10, pady = 5, expand = True)

# Create tabs for the notebook
progress_tab = ctk.CTkFrame(notebook)
progress_tab.pack(expand = True, fill = "both")
downloaded_tab = ctk.CTkFrame(notebook)
downloaded_tab.pack(expand = True, fill = "both")

# Create listbox for downloads in-progress tab
progress_listbox1 = tk.Listbox(progress_tab, background = "lightblue")

# Progress frame
progress_frame = ctk.CTkFrame(progress_listbox1, height= 90, width = 570, border_width = 2)
progress_frame.pack(pady = 10, padx = 5, fill = "both")
progress_frame.pack_propagate(True) # Lock frame size independent of child widgets

progress_vidlabel = ttk.Label(progress_frame,justify = "left", wraplength = 300,
 text = "Video Title downloading .....In progress", style = "progress.TLabel")
progress_vidlabel.pack(side = "left", padx = 10,pady = 10, fill = "both",)

progress_frame.update_idletasks()  #ensures the frame refreshes based on label size.

# Progress Bar


#  Percentage Display (Instead of Progress Bar)
download_progress_value = tk.IntVar(value=0)
percentage_label = tk.Label(progress_frame, text="0%", font=("Arial", 14, "bold"))
percentage_label.pack(side = "left")

# Progress Status
progress_label = tk.Label(progress_frame, text="Waiting to start...")
progress_label.pack()
progress_label.pack(side = "left")


pause_button = ctk.CTkButton(progress_frame, text = "Pause", width = 80 )
pause_button.pack(side = "right", padx = 5)

resume_button = ctk.CTkButton(progress_frame, text = "Resume", width = 80 )
resume_button.pack(side = "right", padx = 5)

progress_listbox1.pack(fill = "both", expand = True)

# Create listbox for downloaded videos tab
downloaded_listbox = tk.Listbox(downloaded_tab, background="orange")
downloaded_listbox.pack(fill = "both", expand = True)

 # Downloaded frame
downloaded_frame = ctk.CTkFrame(downloaded_listbox, height= 90, width = 570, border_width = 2)
downloaded_frame.pack(pady = 10, padx = 5, fill = "both")
downloaded_frame.pack_propagate(False) # Lock frame size independent of child widgets

progress_vidlabel = ctk.CTkLabel(downloaded_frame, text = "Video Title downloading. In progress", bg_color = "orange", compound = "center",)
progress_vidlabel.pack(side = "left", padx = 20)


notebook.add(progress_tab, text = "In Progress")
notebook.add(downloaded_tab, text = "Downloaded")


# notebook.pack(expand=True, fill="both")

root.mainloop()
