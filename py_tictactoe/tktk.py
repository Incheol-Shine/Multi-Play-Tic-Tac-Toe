import tkinter as tk
# from itertools import cycle
from tkinter import font
# from typing import NamedTuple

""" 메뉴바 없이 만들자! """
# window = tk.Tk()
# frame_a = tk.Frame()
# frame_b = tk.Frame()

# label_a = tk.Label(master = frame_a, text = "I'm in frame a")
# label_a.pack()

# label_b = tk.Label(master = frame_b, text = "I'm in frame b")
# label_b.pack()

# frame_a.pack()
# frame_b.pack()

# window.mainloop()

# border_effects = {
#     "flat": tk.FLAT,
#     "sunken": tk.SUNKEN,
#     "raised": tk.RAISED,
#     "groove": tk.GROOVE,
#     "ridge": tk.RIDGE,
# }

# window = tk.Tk()
# for relief_name, relief in border_effects.items():
#     frame = tk.Frame(master=window, relief=relief, borderwidth=5, width=150, height=150)
#     frame.pack(side=tk.LEFT)
#     label = tk.Label(master=frame, text=relief_name)
#     label.place(x=30, y=30)
#     # label.pack()

# frame = tk.Frame(master=window, width=150, height=150)
# frame.pack()
# label1 = tk.Label(master=frame, text="I'm at (34, 34)", bg="yellow")
# label1.place(x=34, y=34)
# label1.pack()


window = tk.Tk()

frame = tk.Frame(master=window, width=500, height=400)
frame.pack()
button = tk.Button(master=frame, text="Click me!", width=20, height=10)
button.place(x=70, y=70)

def handle_click(event):
    print("The button was clicked!")
button.bind("<Button-1>", handle_click)

window.mainloop()

