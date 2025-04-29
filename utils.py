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

# def sanitize_filename(name):
#     # Remove or replace characters that are not allowed in Windows filenames
#     return re.sub(r'[<>:"/\\|?*\u2022]', '', name)

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

