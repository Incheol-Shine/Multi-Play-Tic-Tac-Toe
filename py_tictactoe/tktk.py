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
# 	"flat": tk.FLAT,
# 	"sunken": tk.SUNKEN,
# 	"raised": tk.RAISED,
# 	"groove": tk.GROOVE,
# 	"ridge": tk.RIDGE,
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


# window = tk.Tk()

# frame = tk.Frame(master=window, width=500, height=400)
# frame.pack()
# button = tk.Button(master=frame, text="Click me!", width=20, height=10)
# button.place(x=70, y=70)

# def handle_click(event):
#     print("The button was clicked!")
# button.bind("<Button-1>", handle_click)

# window.mainloop()

############################################################

# window = tk.Tk()
# window.title("frame change")
# window.cells = {}
# menu_bar = tk.Menu(master=window)
# window.config(menu=menu_bar)
# file_menu = tk.Menu(master=menu_bar)
# file_menu.add_command(label="Play Again") #, command=window.reset_board)
# file_menu.add_separator()
# file_menu.add_command(label="Exit", command=quit)
# menu_bar.add_cascade(label="File", menu=file_menu)

# display_frame = tk.Frame(master=window)
# display_frame.pack(fill=tk.X)
# window.display = tk.Label(
# 	master=display_frame,
# 	text="Ready?",
# 	font=font.Font(size=28, weight="bold"),
# )
# window.display.pack()

# grid_frame = tk.Frame(master=window)
# grid_frame.pack()
# for row in range(3):
# 	window.rowconfigure(row, weight=1, minsize=50)
# 	window.columnconfigure(row, weight=1, minsize=75)
# 	for col in range(3):
# 		button = tk.Button(
# 			master=grid_frame,
# 			text="",
# 			font=font.Font(size=36, weight="bold"),
# 			fg="black",
# 			width=3,
# 			height=2,
# 			highlightbackground="lightblue",
# 		)
# 		window.cells[button] = (row, col)
# 		# button.bind("<ButtonPress-1>", window.play)
# 		button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

# window.mainloop()

window = tk.Tk()
window.title("Frame_Change")
window.geometry("600x600+200+200")

frame1 = tk.Frame(window)
frame2 = tk.Frame(window)
frame3 = tk.Frame(window)

frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=0, sticky="nsew")
frame3.grid(row=0, column=0, sticky="nsew")


def openFrame(frame):
	frame.tkraise()

def changeSize():
	window.geometry("400x400")

def changeSize2():
	window.geometry("800x800")

btnToFrame1 = tk.Button(frame3,
			text="Change To Frame1",
			padx=10,
			pady=10,
			command=lambda:[changeSize(), openFrame(frame1)])
			
btnToFrame2 = tk.Button(frame1,
			text="Change To Frame2",
			padx=10,
			pady=10,
			command=lambda:[changeSize2(), openFrame(frame2)])
btnToFrame3 = tk.Button(frame2,
			text="Change To Frame3",
			padx=10,
			pady=10,
			command=lambda:[changeSize(), openFrame(frame3)])

btnToFrame1.pack()
btnToFrame2.pack()
btnToFrame3.pack()

openFrame(frame1)
window.mainloop()


# class TicTacToeBoard(tk.Tk):
# 	def __init__(self):
# 		super().__init__()
# 		self.title("Tic-Tac-Toe Game")
# 		self._cells = {}
# 		self.create_new_frame(size=1)
# 		# self.geometry("800x800")

# 	def create_new_frame(self, size):
# 		self.geometry("800x500")
# 		new_frame = tk.Frame(master=self)
# 		new_frame.pack(expand=True)
# 		new_frame.grid_rowconfigure(0, weight=1)
# 		new_frame.grid_columnconfigure(0, weight=1)

# 		for row in range(size):
# 			self.rowconfigure(row, weight=1, minsize=10)
# 			self.columnconfigure(row, weight=1, minsize=75)
# 			for col in range(size):
# 				button = tk.Button(
# 					master=new_frame,
# 					text="O",
# 					font=font.Font(size=36, weight="bold"),
# 					fg="black",
# 					width=3,
# 					height=2,
# 					highlightbackground="lightblue",
# 				)
# 				self._cells[button] = (row, col)
# 				button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

# window = TicTacToeBoard()
# window.mainloop()