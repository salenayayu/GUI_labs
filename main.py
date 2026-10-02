import tkinter as tk
from PIL import Image, ImageTk

def change_label():
    global photo

    image = Image.open("image_lab1.jpg")

    image = image.resize((250, 250))

    photo = ImageTk.PhotoImage(image)

    label.config(image=photo, text="")

root = tk.Tk()
root.title("Лабораторная работа №1")
root.geometry("400x300")

label = tk.Label(root, text="Ниже волшебная кнопка", font=("Arial", 16))
label.pack(pady=30)

button = tk.Button(root, text="Нажми на меня!", command=change_label,
                   font=("Arial", 12), padx=10, pady=5)
button.pack()

root.mainloop()