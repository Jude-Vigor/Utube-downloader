import re
from tkinter import messagebox

YOUTUBE_REGEX = re.compile(
    r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
)

#play list code
# yt-dlp --ignore-errors --yes-playlist -o "%(playlist_index)s - %(title)s.%(ext)s" "https://www.youtube.com/playlist?list=PL_c9BZzLwBRK0Pc28IdvPQizD2mJlgoID" 


def is_valid_youtube_url(url):
    return bool(YOUTUBE_REGEX.match(url))

def truncate_text(text, max_length=30):
    return text[:max_length] + "..." if len(text) > max_length else text

def show_error(message):
    messagebox.showerror("Error", message)

def sanitize_filename(name):
    # Remove illegal characters first
    name = re.sub(r'[<>:"/\\|?*\u2022]', '', name)
    
    # Remove emojis and any non-ASCII characters
    name = re.sub(r'[^\x00-\x7F]', '', name)
    
    # Remove leading/trailing whitespace and periods
    name = name.strip(' .')
    
    # Collapse multiple spaces into one
    name = re.sub(r'\s+', ' ', name)
    
    return name

