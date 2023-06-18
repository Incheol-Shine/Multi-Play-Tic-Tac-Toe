#from typing import NamedTuple

#class Person(NamedTuple):
#    name: str
#    age: int
#    height: float
#    weight: float
#    country: str = "Canada"


#print(issubclass(Person, tuple))

#jane = Person("Jane", 25, 1.75, 67)
#jane.country = "America"
#print(jane)


#import tkinter as tk

#window = tk.Tk()

#for i in range(3):
#	window.columnconfigure(i, weight=1, minsize=75)
#	window.rowconfigure(i, weight=1, minsize=50)

#	for j in range(0, 3):
#		#frame = tk.Frame(
#		#    master=window,
#		#    relief=tk.RAISED,
#		#    borderwidth=1
#		#)
#		#frame.grid(row=i, column=j, padx=5, pady=5)
#		label = tk.Label(master=window, text=f"Row {i}\nColumn {j}")
#		#label.pack(padx=5, pady=5)
#		label.grid(row=i, column=j, padx=5, pady=5)

#window.mainloop()

#import time
#from threading import Thread, Lock

#def play(args):
#	for i in range(10):
#		print(args)
#		time.sleep(1)
#	lock.acquire()
#	for i in range(3):
#		print(args + 10)
#		time.sleep(1)
#	lock.release()

#lock = Lock()
#t1 = Thread(target=play, args=(1,))
#t1.start()
#play(0)

#import time
#from threading import Thread, Lock
#import socket

#HOST = '127.0.0.1'
#PORT = 12346

#class	ThreadRecv(Thread):
#	def __init__(self, c_socket, daemon=False):
#		super().__init__(daemon=daemon)
#		self.c_socket = c_socket
#		self.stop_flag = False
	
#	def run(self):
#		while not(self.stop_flag):
#			#coord = self.c_socket.recv(10).decode()
#			msg = "Ho"
#			data = msg.encode('utf-8')
#			self.c_socket.send(data)
#			print("he")
#			time.sleep(1)

#	def stop(self):
#		self.stop_flag = True

#clnt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#clnt_socket.connect((HOST, PORT))
##t1 = ThreadRecv(c_socket=clnt_socket, daemon=True)
#t1 = ThreadRecv(c_socket=clnt_socket)
#t1.start()
#time.sleep(3)
#t1.stop()
#clnt_socket.close()

import tkinter as tk
from tkinter import font
import time

class	Main(tk.Tk):
	def __init__(self,):
		super().__init__()
		self.title("Tic-Tac-Toe Game")
		self._cells = {}
		self._create_menu()
		self._create_board_display()

	def _create_menu(self):
		menu_bar = tk.Menu(master=self)
		self.config(menu=menu_bar)
		file_menu = tk.Menu(master=menu_bar)
		file_menu.add_command(label="Play Again", command=self.f)
		file_menu.add_separator()
		file_menu.add_command(label="Exit", command=quit)
		menu_bar.add_cascade(label="File", menu=file_menu)

	def _create_board_display(self):
		display_frame = tk.Frame(master=self)
		display_frame.pack(fill=tk.X)
		self.display = tk.Label(
			master=display_frame,
			text="Ready?",
			font=font.Font(size=28, weight="bold"),
		)
		self.display.pack()
	
	def f(self):
		for _ in range(4):
			time.sleep(3)
			print("yolo")

window = Main()
window.mainloop()
