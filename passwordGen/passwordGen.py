import tkinter as tk
from tkinter import ttk, filedialog
import re

def replace_letters(phrase):
    replacements = {
        'O': '0', 'I': '1', 'L': '1', '7': '1', '|': '1', '!': '1',
        'Z': '2', 'E': '3', 'h': '4', 'A': '4', 'y': '4',
        'S': '5', 'b': '6', 'G': '6', 'T': '7', 'K': '7',
        'B': '8', 'X': '8', 'g': '9', 'J': '9', 'P': '9',
        'N': '11', '||': '11', 'R': '12'
    }

    for key, value in replacements.items():
        phrase = re.sub(re.escape(key), value, phrase, flags=re.IGNORECASE)

    return phrase

def calculate_strength(password):
    length = len(password)
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[\W_]', password))
    
    strength = length >= 8 and has_upper and has_lower and has_digit and has_special
    return "Strong" if strength else "Weak"

def generate_password():
    phrase = phrase_entry.get()
    if not phrase:
        password_label.config(text="Please enter a phrase")
        strength_label.config(text="")
        return
    phrase = replace_letters(phrase)
    
    if add_star.get() == "beginning":
        phrase = '*' + phrase
    elif add_star.get() == "end":
        phrase = phrase + '*'
        
    if add_dash.get() == "beginning":
        phrase = '-' + phrase
    elif add_dash.get() == "end":
        phrase = phrase + '-'
    
    password_label.config(text=phrase)
    strength_label.config(text=f"Password Strength: {calculate_strength(phrase)}")

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_label.cget("text"))

def clear_fields():
    phrase_entry.delete(0, tk.END)
    password_label.config(text="")
    strength_label.config(text="")

def save_to_file():
    password = password_label.cget("text")
    if password:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(password)

# Setup Tkinter window
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x400")
root.configure(padx=20, pady=20)

# Phrase entry frame
phrase_frame = tk.Frame(root)
phrase_frame.pack(fill="x", pady=10)

tk.Label(phrase_frame, text="Enter Phrase:", font=("Helvetica", 12)).pack(side="left", padx=10)
phrase_entry = tk.Entry(phrase_frame, width=50)
phrase_entry.pack(side="left", padx=10)

# Special characters frame
special_char_frame = tk.Frame(root)
special_char_frame.pack(fill="x", pady=10)

tk.Label(special_char_frame, text="Special Characters:", font=("Helvetica", 12)).pack(anchor="w", padx=10, pady=5)

add_star = tk.StringVar(value="none")
add_dash = tk.StringVar(value="none")

star_frame = tk.Frame(special_char_frame)
star_frame.pack(anchor="w", padx=20)

tk.Label(star_frame, text="Add *:", font=("Helvetica", 10)).pack(side="left", padx=5)
tk.Radiobutton(star_frame, text="None", variable=add_star, value="none").pack(side="left")
tk.Radiobutton(star_frame, text="Beginning", variable=add_star, value="beginning").pack(side="left")
tk.Radiobutton(star_frame, text="End", variable=add_star, value="end").pack(side="left")

dash_frame = tk.Frame(special_char_frame)
dash_frame.pack(anchor="w", padx=20, pady=5)

tk.Label(dash_frame, text="Add -:", font=("Helvetica", 10)).pack(side="left", padx=5)
tk.Radiobutton(dash_frame, text="None", variable=add_dash, value="none").pack(side="left")
tk.Radiobutton(dash_frame, text="Beginning", variable=add_dash, value="beginning").pack(side="left")
tk.Radiobutton(dash_frame, text="End", variable=add_dash, value="end").pack(side="left")

# Buttons frame
button_frame = tk.Frame(root)
button_frame.pack(fill="x", pady=10)

generate_button = tk.Button(button_frame, text="Generate Password", command=generate_password)
generate_button.pack(side="left", padx=5)

copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(side="left", padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_fields)
clear_button.pack(side="left", padx=5)

save_button = tk.Button(button_frame, text="Save to File", command=save_to_file)
save_button.pack(side="left", padx=5)

# Password display frame
password_frame = tk.Frame(root)
password_frame.pack(fill="x", pady=10)

password_label = tk.Label(password_frame, text="", font=("Helvetica", 12))
password_label.pack(pady=5)

# Password strength frame
strength_frame = tk.Frame(root)
strength_frame.pack(fill="x", pady=10)

strength_label = tk.Label(strength_frame, text="", font=("Helvetica", 12))
strength_label.pack(pady=5)

root.mainloop()
