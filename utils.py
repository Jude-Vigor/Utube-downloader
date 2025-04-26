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

def sanitize_filename(name):
    # Remove or replace characters that are not allowed in Windows filenames
    return re.sub(r'[<>:"/\\|?*\u2022]', '', name)
    

# # ✅ Catch audio or non-merged downloads
# if "[download]" in line and "Destination:" in line:
#     match = re.search(r'Destination:\s+(.+)', line)
#     if match:
#         final_path = match.group(1).strip()
#         print("✅ Audio file path detected:", final_path)
#             #  Detect merged final file