import tkinter as tk
from tkinter import font
from itertools import cycle
import time

def counter(window):
	frame0 = tk.Frame(master=window)
	frame0.pack(fill=tk.BOTH, expand=1)
	frame1 = tk.Frame(master=frame0)
	frame1.pack(fill=tk.BOTH, expand=1)
	display = tk.Label(master=frame1,
					text="Counter",
					font=font.Font(size=20, weight="bold"))
	display.pack(fill=tk.BOTH, expand=1)
	number = tk.Label(master=frame1,
					text="0",
					font=font.Font(size=28, weight="bold"))
	number.pack(fill=tk.BOTH, expand=1)
	frame2 = tk.Frame(master=frame0)
	frame2.pack(fill=tk.BOTH, expand=1)
	frame2.rowconfigure(0, minsize=50, weight=1)
	frame2.columnconfigure([0, 1, 2], minsize=50, weight=1)

	def decrease():
		value = int(number["text"])
		if (value > 0):
			number["text"] = f"{value - 1}"

	def reset():
		number["text"] = "0"

	def increase():
		value = int(number["text"])
		if (value < 10):
			number["text"] = f"{value + 1}"


	btnDecrease=tk.Button(master=frame2,
					text="-",
					font=font.Font(size=15, weight="normal"),
	                command=decrease)
	btnDecrease.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

	btnReset=tk.Button(master=frame2,
					text="Reset",
					font=font.Font(size=15, weight="normal"),
					command=reset)
	btnReset.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

	btnIncrease=tk.Button(master=frame2,
					text="+",
					font=font.Font(size=15, weight="normal"),
					command=increase)
	btnIncrease.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

	return 0

class	MainFrame(tk.Tk):
	def __init__(self):
		super().__init__()
		self.frames = cycle([Frame0(self), Frame2(self)])
		self.cur_frame = next(self.frames)

	def change_frame(self):
		self.cur_frame.forget()
		self.cur_frame = next(self.frames)
		self.cur_frame.tkraise()
		self.cur_frame.pack(padx=50, pady=50, fill=tk.BOTH, expand=1)

class	Frame0(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.pack(padx=50, pady=50, fill=tk.BOTH, expand=1)
		self.title = tk.Label(master=self,
			text="Tic Tac Toe",
			font=font.Font(size=28, weight="bold"))
		self.title.pack(padx=50, pady=50)
		self.btnPlay = tk.Button(master=self,
			   text="Play",
			   font=font.Font(size=20, weight="bold"),
			   command=parent.change_frame)
		self.btnPlay.pack(padx=50, pady=50, expand=1)

class	Frame1(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.display = tk.Label(master=self,
			  text="Match Making...",
			  font=font.Font(size=28, weight="bold"))
		self.display.pack(pady=50)


class	Frame2(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.display = tk.Label(master=self,
			  text="Your Turn",
			  font=font.Font(size=28, weight="bold"))
		self.display.pack()
		self.btnPopUpFrame = tk.Frame(master=self)
		button = tk.Button(master=self.btnPopUpFrame,
		     text="Retry?",
			 font=font.Font(size=20, weight="bold"),
			 command=lambda:[self.changeFrmae1(), parent.change_frame()])
		button.pack()
		self.gridFrame = tk.Frame(master=self)
		self.gridFrame.pack()
		self.gridFrame.grid_rowconfigure(0, weight=1)
		self.gridFrame.grid_columnconfigure(0, weight=1)
		self._cells = {}
		
		for row in range(3):
			self.gridFrame.rowconfigure(row, weight=1, minsize=10)
			self.gridFrame.columnconfigure(row, weight=1, minsize=75)
			for col in range(3):
				button = tk.Button(
					master=self.gridFrame,
					text="",
					font=font.Font(size=36, weight="bold"),
					fg="black",
					width=3,
					height=2,
					highlightbackground="lightblue",
					command=self.changeFrame2
				)
				self._cells[button] = (row, col)
				button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

	def changeFrmae1(self):
		self.btnPopUpFrame.forget()

	def changeFrame2(self):
		self.gridFrame.forget()
		self.btnPopUpFrame.tkraise()
		self.btnPopUpFrame.pack()
		self.gridFrame.tkraise()
		self.gridFrame.pack()


if __name__ == "__main__":
	window = MainFrame()
	window.geometry("+950+200")
	window.mainloop()
