import re
from tkinter import messagebox
import unicodedata


YOUTUBE_REGEX = re.compile(
    r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
)

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

 # Check reserved names
    reserved_names = {"CON", "PRN", "AUX", "NUL",
                      *(f"COM{i}" for i in range(1, 10)),
                      *(f"LPT{i}" for i in range(1, 10))}
    if name.upper().split('.')[0] in reserved_names:
        name = f"_{name}"
    
    return name[:200]

#Alternative to sanitize_name// not being used atm, might be needed later
def clean_filename(filename):
    # Remove emojis and non-ASCII characters
    filename = unicodedata.normalize('NFKD', filename)
    filename = filename.encode('ascii', 'ignore').decode('ascii')

    # Remove leftover bad characters
    filename = re.sub(r'[\\/*?:"<>|]', '', filename)

    # Optionally limit length again
    return filename[:200]
