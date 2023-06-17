
from threading import Thread, Lock
from time import sleep
import tkinter as tk
from tkinter import font
from itertools import cycle
import socket
from typing import NamedTuple

class Player(NamedTuple):
	label: str
	color: str

class Move(NamedTuple):
	row: int
	col: int
	label: str = ""

HOST = '127.0.0.1'
PORT = 12347
BOARD_SIZE = 3
DEFAULT_PLAYERS = (
	Player(label="X", color="blue"),
	Player(label="O", color="green"),
)

""" Frame 2 에서 Frame 3 로 전환할 때, recv()에서 멈춰서 화면전환이 안되는 현상을 방지하기 위해 새 스레드를 만듭니다. """
class	ThreadMatchMake(Thread):
	def __init__(self, clnt_socket, main_frame, daemon=False):
		super().__init__(daemon=daemon)
		self.clnt_socket = clnt_socket
		self.main_frame = main_frame
		self.thread_running = True
	
	def run(self):
		self.clnt_socket.recv(3).decode()
		print("yeah recv perfactly")
		self.main_frame.change_frame()
		while (self.thread_running):
			print("thread recv...")
			coord = self.clnt_socket.recv(3).decode()
			print(f"coord : {coord}")
			row, col = map(int, (coord.split()))
			print(f"{row}")
			self.main_frame.frames[2].play(row=row, col=col)
			print(f"recv row:{row}, col:{col}!")

	def stop(self):
		self.thread_running = False


class	SocketHandler():
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.clnt_socket = None
		self.my_symbol = None
		self.recv_thread = None

	""" 게임 시작 후, 서버에 연결하는 소켓을 생성합니다. 그리고 Frame 1 에서 Frame 2 로 화면을 전환합니다.
		서버가 응답하면 서버에서 전송한 플레이어의 마크 ("X", "O") 를 저장합니다.
		매칭 상대를 기다리다가 매칭이 되면 화면을 전환하는 새로운 스레드를 생성하고 해당 함수는 종료합니다. """
	def open_socket(self, main_frame):
		self.clnt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clnt_socket.connect((self.host, self.port))
		self.my_symbol = str(self.clnt_socket.recv(3).decode())
		self.frame = main_frame
		self.frame.change_frame()
		print(self.my_symbol)
		self.recv_coord()

	def get_my_symbol(self):
		return self.my_symbol

	def recv_coord(self):
		self.recv_thread = ThreadMatchMake(self.clnt_socket, self.frame)
		self.recv_thread.start()
	
	def send_coord(self, row, col):
		coord = f"{row} {col}"
		data = coord.encode('utf-8')
		self.clnt_socket.send(data)
		print(f"{sh.get_my_symbol()}'s turn! send msg!")
	
	def close_socket(self):
		self.recv_thread.stop()
		self.clnt_socket.close()

class	GamePlay():
	def __init__(self):
		return

class TicTacToeGame:
	def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
		self._players = cycle(players)
		self.board_size = board_size
		self.current_player = next(self._players)
		self.winner_combo = []
		self._current_moves = []
		self._has_winner = False
		self._winning_combos = []
		self._setup_board()

	def _setup_board(self):
		self._current_moves = [
			[Move(row, col) for col in range(self.board_size)]
			for row in range(self.board_size)
		]
		self._winning_combos = self._get_winning_combos()

	def _get_winning_combos(self):
		rows = [
			[(move.row, move.col) for move in row]
			for row in self._current_moves
	    ]
		columns = [list(col) for col in zip(*rows)]
		first_diagonal = [row[i] for i, row in enumerate(rows)]
		second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
		return rows + columns + [first_diagonal, second_diagonal]

	def toggle_player(self):
		"""Return a toggled player."""
		self.current_player = next(self._players)

	def is_valid_move(self, move):
		"""Return True if move is valid, and False otherwise."""
		row, col = move.row, move.col
		move_was_not_played = self._current_moves[row][col].label == ""
		no_winner = not self._has_winner
		
		return no_winner and move_was_not_played

	def process_move(self, move):
		"""Process the current move and check if it's a win."""
		row, col = move.row, move.col
		self._current_moves[row][col] = move
		for combo in self._winning_combos:
			results = set(self._current_moves[n][m].label for n, m in combo)
			is_win = (len(results) == 1) and ("" not in results)
			if is_win:
				self._has_winner = True
				self.winner_combo = combo
				break

	def has_winner(self):
		"""Return True if the game has a winner, and False otherwise."""
		return self._has_winner

	def is_tied(self):
		"""Return True if the game is tied, and False otherwise."""
		no_winner = not self._has_winner
		played_moves = (
		    move.label for row in self._current_moves for move in row
		)
		return no_winner and all(played_moves)

	def reset_game(self):
		"""Reset the game state to play again."""
		for row, row_content in enumerate(self._current_moves):
			for col, _ in enumerate(row_content):
				row_content[col] = Move(row, col)
		self._has_winner = False
		self.winner_combo = []
	
	def is_my_turn(self):
		print("my_turn?")
		print(f"current : {self.current_player.label}, my_symbol:{sh.get_my_symbol()}")
		print(self.current_player.label in sh.get_my_symbol())
		return (self.current_player.label in sh.get_my_symbol())


class	MainFrame(tk.Tk):
	def __init__(self, game):
		super().__init__()
		self._frame_idx = 0
		self.frames = [Frame0(self), Frame1(self), Frame2(self, game)]
		self.cur_frame = self.frames[self._frame_idx]

	def change_frame(self):
		""" 현재 프레임을 숨기고 다음 프레임을 올립니다. """
		self.cur_frame.forget()
		self._frame_idx = (self._frame_idx + 1) % 3
		self.cur_frame = self.frames[self._frame_idx]
		self.frames[2].update_display(msg=f"You are {sh.get_my_symbol()}")
		self.cur_frame.tkraise()
		self.cur_frame.pack(padx=50, pady=50, fill=tk.BOTH, expand=1)

class	Frame0(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		self.pack(padx=50, pady=50, fill=tk.BOTH, expand=1)
		self._create_display()
		self._create_play_btn()
	
	def	_create_display(self):
		self.title = tk.Label(master=self,
			text="Tic Tac Toe",
			font=font.Font(size=28, weight="bold"))
		self.title.pack(padx=50, pady=50)

	def _create_play_btn(self):
		self.play_btn = tk.Button(master=self,
			   text="Play",
			   font=font.Font(size=20, weight="bold"),
			   command=lambda:[sh.open_socket(self.parent)])
		self.play_btn.pack(padx=50, pady=50, expand=1)

class	Frame1(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self._create_display()

	def _create_display(self):
		self.display = tk.Label(master=self,
			  text="Match Making...",
			  font=font.Font(size=28, weight="bold"))
		self.display.pack(pady=50)


class	Frame2(tk.Frame):
	def __init__(self, parent, game):
		super().__init__(parent)
		self.parent = parent
		self._game = game
		self._cells = {}
		self._convert_cells = {}
		self.is_game_reset = False
		self._create_display()
		self._create_pop_up_btn_frame()
		self._create_grid_frame()

	def _create_display(self):
		self.display = tk.Label(master=self,
			  text="",
			  font=font.Font(size=28, weight="bold"))
		self.display.pack()
	
	def _create_pop_up_btn_frame(self):
		self.btnPopUpFrame = tk.Frame(master=self)
		button = tk.Button(master=self.btnPopUpFrame,
		     text="Retry?",
			 font=font.Font(size=20, weight="bold"),
			 command=lambda:[self.changeFrame1(), 
		    					self.parent.change_frame(),
								self.reset_board()])
		button.pack()
	
	def _create_grid_frame(self):
		self.gridFrame = tk.Frame(master=self)
		self.gridFrame.pack()
		self.gridFrame.grid_rowconfigure(0, weight=1)
		self.gridFrame.grid_columnconfigure(0, weight=1)
		
		for row in range(3):
			self.gridFrame.rowconfigure(row, weight=1, minsize=50)
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
				)
				self._cells[button] = (row, col)
				button.bind("<ButtonPress-1>", lambda event: self.play(event, None) )
				button.grid(row=row, column=col, padx=5, pady=5)
		self._convert_cells = {v:k for k,v in self._cells.items()}

	def changeFrame1(self):
		self.btnPopUpFrame.forget()

	def popUpRetry(self):
		self.gridFrame.forget()
		self.btnPopUpFrame.tkraise()
		self.btnPopUpFrame.pack()
		self.gridFrame.tkraise()
		self.gridFrame.pack()

	def play(self, event=None, row=None, col=None):
		"""Handle a player's move."""
		if (row == None):
			if not(self._game.is_my_turn()):
				return
			clicked_btn = event.widget
		else:
			clicked_btn = self._convert_cells[(row, col)]

		lock.acquire()
		row, col = self._cells[clicked_btn]
		move = Move(row, col, self._game.current_player.label)
		if self._game.is_valid_move(move):
			if (self._game.is_my_turn()):
				sh.send_coord(row, col)
			self._update_button(clicked_btn)
			self._game.process_move(move)
			if self._game.is_tied():
				self.update_display(msg="Tied game!", color="red")
				self.popUpRetry()
			elif self._game.has_winner():
				self._highlight_cells()
				msg = f'Player "{self._game.current_player.label}" won!'
				color = self._game.current_player.color
				self.update_display(msg, color)
				self.popUpRetry()
			else:
				self._game.toggle_player()
				msg = f"{self._game.current_player.label}'s turn"
				self.update_display(msg)
		lock.release()

	def _update_button(self, clicked_btn):
		clicked_btn.config(text=self._game.current_player.label)
		clicked_btn.config(fg=self._game.current_player.color)

	def update_display(self, msg, color="black"):
		self.display["text"] = msg
		self.display["fg"] = color

	def _highlight_cells(self):
		for button, coordinates in self._cells.items():
			if coordinates in self._game.winner_combo:
				button.config(highlightbackground="red")

	def reset_board(self):
		"""Reset the game's board to play again."""
		self._game.reset_game()
		sh.close_socket()
		for button in self._cells.keys():
			button.config(highlightbackground="lightblue")
			button.config(text="")
			button.config(fg="black")

lock = Lock()
sh = SocketHandler(HOST, PORT)
game = TicTacToeGame()
window = MainFrame(game)
window.geometry("720x800+1000+400")
window.mainloop()
