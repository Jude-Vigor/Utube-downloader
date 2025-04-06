import tkinter as tk

# Main top-level window
root = tk.Tk()
root.title("Main Window")

# Secondary top-level window
secondary = tk.Toplevel(root)
secondary.title("Secondary Window")

root.mainloop()