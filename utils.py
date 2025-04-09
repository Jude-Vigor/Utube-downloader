import re
from tkinter import messagebox

YOUTUBE_REGEX = re.compile(
    r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
)

def is_valid_youtube_url(url):
    return bool(YOUTUBE_REGEX.match(url))

def truncate_text(text, max_length=30):
    return text[:max_length] + "..." if len(text) > max_length else text

def show_error(message):
    messagebox.showerror("Error", message)

