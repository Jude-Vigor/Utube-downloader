def truncate_text(text,max_length = 30):
    return text[:max_length] + "..." if len(text) > max_length else text
