from tkinter import *
from tkinter import filedialog, messagebox
from deep_translator import GoogleTranslator
import pyttsx3
from PIL import Image, ImageTk
import threading
import datetime

Engine = pyttsx3.init()

# Initialize the main window
window = Tk()
window.config(bg="black", borderwidth=2, relief="solid")
window.title("Notepad+")
window.geometry("500x500")
window.resizable(0, 0)
menu = Menu(window)
window.config(menu=menu)

def load_webp_image(filepath, size):
    # Load the .webp image
    image = Image.open(filepath)
    # Resize the image
    image = image.resize(size, Image.Resampling.LANCZOS)
    # Convert to PhotoImage
    return ImageTk.PhotoImage(image)

# Load and resize icons (assuming you have your .webp icons in the icons folder)
icon_size = (20, 20)  # Desired icon size
save_icon = load_webp_image("save-64.webp", icon_size)
open_icon = load_webp_image("folder-open-64.webp", icon_size)
new_icon = load_webp_image("__add_new_plus-64.webp", icon_size)
exit_icon = load_webp_image("exit.webp", icon_size)
translate_icon = load_webp_image("google_translate.webp", icon_size)
read_icon = load_webp_image("pronouncer.png", icon_size)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get("1.0", END))

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete("1.0", END)
            content = file.read()
            text_area.insert(END, content)

def new_file():
    text_area.delete("1.0", END)

def exit_app():
    if messagebox.askyesno("Exit", "Do you want to exit?"):
        window.destroy()

def translate_text(language):
    try:
        text = text_area.get("1.0", END).strip()
        if text:
            translated = GoogleTranslator(source='auto', target=language).translate(text)
            translation_window = Toplevel(window)
            translation_window.geometry("500x500")
            label = Label(translation_window, text=translated, wraplength=400)
            label.pack()
        else:
            messagebox.showwarning("Empty Input", "Please enter some text to translate.")
    except Exception as e:
        messagebox.showwarning("Something Went Wrong", f"Due to a network issue, the text could not be translated. Sorry! 😒😒\n\nError: {e}")

def translate_to_fr():
    translate_text("fr")

def translate_to_hi():
    translate_text("hi")

def translate_to_kn():
    translate_text("kn")

def read_text():
    text = text_area.get("1.0", END)
    thread = threading.Thread(target=speak_text, args=(text,))
    thread.start()

def speak_text(text):
    Engine.say(text)
    Engine.runAndWait()

def update_time():
    current_time = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    label2.config(text=f"Notepad+                    {current_time}")
    window.after(1000, update_time)  # Update every 1000 milliseconds (1 second)

# Create menu labels and functions
file_menu = Menu(menu, tearoff=0)
edit_menu = Menu(menu, tearoff=0)
read_menu = Menu(menu, tearoff=0)

menu.add_cascade(label="FILE", menu=file_menu, font="Lucida")
menu.add_cascade(label="TRANSLATE", menu=edit_menu, font="Lucida")
menu.add_cascade(label="PRONOUNCE", menu=read_menu, font="Lucida")

file_menu.add_command(label="SAVE", image=save_icon, compound=LEFT, background="#CCCCCC", command=save_file)
file_menu.add_command(label="OPEN", image=open_icon, compound=LEFT, background="#CCCCCC", command=open_file)
file_menu.add_command(label="NEW", image=new_icon, compound=LEFT, background="#CCCCCC", command=new_file)
file_menu.add_command(label="EXIT", image=exit_icon, compound=LEFT, background="#CCCCCC", command=exit_app)

edit_menu.add_command(label="To_FRA", image=translate_icon, compound=LEFT, background="#CCCCCC", command=translate_to_fr)
edit_menu.add_command(label="TO_HIN", image=translate_icon, compound=LEFT, background="#CCCCCC", command=translate_to_hi)
edit_menu.add_command(label="TO_KAN", image=translate_icon, compound=LEFT, background="#CCCCCC", command=translate_to_kn)

read_menu.add_command(label="READ", image=read_icon, compound=LEFT, background="#CCCCCC", command=read_text)

# Create text area and labels
label2 = Label(window, text="----------CURRENT DATETIME  -------------------", bg="black", fg="white", font=("Consolas", 12))
label2.pack()

text_area = Text(window, bg="black", fg="green", font="Consolas", cursor="xterm", insertbackground="grey", insertwidth=2)
text_area.pack()

label3 = Label(window, text="--------------------------------------------------------------------", fg="white", bg="black")
label3.pack()

update_time()  # Call the update_time function to start the timer
window.mainloop()
