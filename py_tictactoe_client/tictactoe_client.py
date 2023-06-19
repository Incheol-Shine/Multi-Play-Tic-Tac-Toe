
from threading import Thread, Lock
import tkinter as tk
from tkinter import font
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
PORT = 12345
BOARD_SIZE = 3
DEFAULT_PLAYERS = (
	Player(label="X", color="blue"),
	Player(label="O", color="green"),
)

""" Frame 2 에서 Frame 3 로 전환할 때, recv()에서 멈춰서 화면 전환이 안 되는 현상을 방지하기 위해 새 스레드를 만듭니다. """
class	ThreadMatchMake(Thread):
	def __init__(self, clnt_socket, main_frame, daemon=False):
		super().__init__(daemon=daemon)
		self.clnt_socket = clnt_socket
		self.main_frame = main_frame
		self.thread_running = True
	
	""" 서버에서 매칭 완료 메시지를 받으면 Frame 3 으로 전환합니다. 이후 반복문 안에서 좌표정보를 수신합니다. """
	def run(self):
		self.clnt_socket.recv(3).decode()
		self.main_frame.change_frame()
		while (self.thread_running):
			coord = self.clnt_socket.recv(3).decode()				
			row, col = map(int, (coord.split()))
			self.main_frame.frames[2].play(row=row, col=col)

	""" 스레드의 반복문을 탈출하고 스레드를 종료합니다. """
	def stop(self):
		self.thread_running = False

""" 서버와의 소켓통신을 관리하는 클래스입니다. """
class	SocketHandler():
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.clnt_socket = None
		self.my_symbol = None
		self.recv_thread = None

	""" 게임 시작 후, 서버에 연결하는 소켓을 생성합니다. 그리고 Frame 1 에서 Frame 2 로 화면을 전환합니다.
		서버가 응답하면 서버에서 전송한 플레이어의 심볼 ("X", "O") 를 저장합니다.
		매칭 상대를 기다리다가 매칭이 되면 화면을 전환하는 새로운 스레드를 생성하고 해당 함수는 종료합니다. """
	def open_socket(self, main_frame):
		self.clnt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clnt_socket.connect((self.host, self.port))
		self.my_symbol = str(self.clnt_socket.recv(3).decode())
		self.frame = main_frame
		self.frame.change_frame()
		self.recv_msg()

	""" 플레이어의 심볼을 반환합니다. """
	def get_my_symbol(self):
		return self.my_symbol

	""" 서버로부터 메세지를 수신하기 위해 새 스레드를 엽니다. """
	def recv_msg(self):
		self.recv_thread = ThreadMatchMake(self.clnt_socket, self.frame, daemon=True)
		self.recv_thread.start()
	
	""" 서버로 데이터를 전송합니다. """
	def send_msg(self, msg):
		data = msg.encode('utf-8')
		self.clnt_socket.send(data)
	
	""" 게임이 끝났다는 메시지를 서버에 전송합니다. """
	def close_socket(self):
		self.send_msg("end\0")
		self.recv_thread.stop()
		self.clnt_socket.close()

""" 게임 진행에 필요한 정보들을 관리하는 클래스입니다. """
class TicTacToeGame:
	def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
		self._players = players
		self.board_size = board_size
		self._player_idx = 0
		self.current_player = self._players[self._player_idx]
		self.winner_combo = []
		self._current_moves = []
		self._has_winner = False
		self._winning_combos = []
		self._setup_board()

	""" 틱택토 게임판의 초기 상태를 세팅합니다. (전부 비어있는 상태) """
	def _setup_board(self):
		self._current_moves = [
			[Move(row, col) for col in range(self.board_size)]
			for row in range(self.board_size)
		]
		self._winning_combos = self._get_winning_combos()

	""" 승리의 조건을 담은 리스트입니다. 8*3 크기의 이차원 리스트를 반환합니다. 한 행의 세 좌표가 같은 모양이면 승리입니다. """
	def _get_winning_combos(self):
		rows = [
			[(move.row, move.col) for move in row]
			for row in self._current_moves
	    ]
		columns = [list(col) for col in zip(*rows)]
		first_diagonal = [row[i] for i, row in enumerate(rows)]
		second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
		return rows + columns + [first_diagonal, second_diagonal]

	""" 다음 차례의 플레이어로 전환합니다. """
	def toggle_player(self):
		self._player_idx = (self._player_idx + 1) % 2
		self.current_player = self._players[self._player_idx]

	""" 현재 참가자의 행동이 유효하면 True 를, 아니면 False 를 반환합니다. """
	def is_valid_move(self, move):
		row, col = move.row, move.col
		move_was_not_played = self._current_moves[row][col].label == ""
		no_winner = not self._has_winner
		return no_winner and move_was_not_played

	""" 현채 참가자의 행동을 적용하고, 승리조건에 해당하는지 확인합니다. """
	def process_move(self, move):
		row, col = move.row, move.col
		self._current_moves[row][col] = move
		for combo in self._winning_combos:
			results = set(self._current_moves[n][m].label for n, m in combo)
			is_win = (len(results) == 1) and ("" not in results)
			if is_win:
				self._has_winner = True
				self.winner_combo = combo
				break

	""" 승리자가 나왔을 경우 True, 아니면 False 를 반환합니다. """
	def has_winner(self):
		return self._has_winner

	""" 게임이 비겼을 경우 True, 아니면 False 를 반환합니다. """
	def is_tied(self):
		no_winner = not self._has_winner
		played_moves = (
		    move.label for row in self._current_moves for move in row
		)
		return no_winner and all(played_moves)

	""" 게임 재시작을 위해 리셋합니다. """
	def reset_game(self):
		for row, row_content in enumerate(self._current_moves):
			for col, _ in enumerate(row_content):
				row_content[col] = Move(row, col)
		self._has_winner = False
		self.winner_combo = []
		self._player_idx = 0
		self.current_player = self._players[self._player_idx]
	
	""" 현재 자신의 차례이면 True, 아니면 False 를 반환합니다. """
	def is_my_turn(self):
		return (self.current_player.label in sh.get_my_symbol())

""" 게임 화면을 관리하는 클래스입니다. """
class	MainFrame(tk.Tk):
	def __init__(self, game):
		super().__init__()
		self._frame_idx = 0
		self.frames = [Frame0(self), Frame1(self), Frame2(self, game)]
		self.cur_frame = self.frames[self._frame_idx]

	""" 현재 프레임을 숨기고 다음 프레임으로 전환합니다. """
	def change_frame(self):
		self.cur_frame.forget()
		self._frame_idx = (self._frame_idx + 1) % 3
		self.cur_frame = self.frames[self._frame_idx]
		self.frames[2].update_display(msg=f"You are {sh.get_my_symbol()}")
		self.cur_frame.tkraise()
		self.cur_frame.pack(padx=50, pady=50, fill=tk.BOTH, expand=1)

""" 게임 실행시 첫번째로 보여지는 화면입니다. Tic Tac Toe 제목과 Play 버튼으로 구성됩니다."""
class	Frame0(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		self.pack(padx=50, pady=50, fill=tk.BOTH, expand=1)
		self._create_display()
		self._create_play_btn()
	
	""" 제목(Tic Tac Toe)을 생성합니다. """
	def	_create_display(self):
		self.title = tk.Label(master=self,
			text="Tic Tac Toe",
			font=font.Font(size=28, weight="bold"))
		self.title.pack(padx=50, pady=50)

	""" Play 버튼을 생성합니다. 버튼을 누르면 서버와 연결하고 매칭이 시작됩니다. """
	def _create_play_btn(self):
		self.play_btn = tk.Button(master=self,
			   text="Play",
			   font=font.Font(size=20, weight="bold"),
			   command=lambda:[sh.open_socket(self.parent)])
		self.play_btn.pack(padx=50, pady=50, expand=1)

""" 게임의 두번째 화면입니다. 매칭 중이라는 메시지를 출력합니다. """
class	Frame1(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self._create_display()

	def _create_display(self):
		self.display = tk.Label(master=self,
			  text="Match Making...",
			  font=font.Font(size=26, weight="bold"))
		self.display.pack(pady=50)

""" 게임의 세번째 화면입니다. 본격적으로 틱택토 게임이 진행됩니다. """
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

	""" 플레이어의 심볼을 알려주고, 누구의 차례인지를 화면에 출력합니다. """
	def _create_display(self):
		self.display = tk.Label(master=self,
			  text="",
			  font=font.Font(size=26, weight="bold"))
		self.display.pack()
	
	""" 게임 재시작 버튼을 생성합니다. 처음엔 가려져있다가 게임 종료시 나타납니다. """
	def _create_pop_up_btn_frame(self):
		self.btnPopUpFrame = tk.Frame(master=self)
		button = tk.Button(master=self.btnPopUpFrame,
		     text="Retry?",
			 font=font.Font(size=20, weight="bold"),
			 command=lambda:[self._hide_retry_btn(), 
		    					self.parent.change_frame(),
								self.reset_board()])
		button.pack()
	
	""" 틱택토 게임판을 생성합니다. """
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

	""" retry 버튼을 숨깁니다. """
	def _hide_retry_btn(self):
		self.btnPopUpFrame.forget()

	""" retry 버튼이 나타나게 합니다. """
	def popUpRetry(self):
		self.gridFrame.forget()
		self.btnPopUpFrame.tkraise()
		self.btnPopUpFrame.pack()
		self.gridFrame.tkraise()
		self.gridFrame.pack()

	""" 플레이어의 행동(버튼 클릭), 상대 플레이어의 행동(서버에서 받은 좌표) 에 따라 게임을 진행시킵니다. """
	def play(self, event=None, row=None, col=None):
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
				sh.send_msg(f"{row} {col}")
			self._update_button(clicked_btn)
			self._game.process_move(move)
			if self._game.is_tied():
				self.update_display(msg="Tied game!", color="red")
				self.end_game()
			elif self._game.has_winner():
				self._highlight_cells()
				msg = f'Player "{self._game.current_player.label}" won!'
				color = self._game.current_player.color
				self.update_display(msg, color)
				self.end_game()
			else:
				self._game.toggle_player()
				msg = f"{self._game.current_player.label}'s turn"
				self.update_display(msg)
		lock.release()

	""" 게임이 끝났을 때, retry 버튼을 보이게 하고 소켓통신을 종료합니다. """
	def end_game(self):
		self.popUpRetry()
		sh.close_socket()

	""" 플레이어의 행동이 진행되었을 때 버튼 위에 해당 플레이어의 심볼을 출력합니다. """
	def _update_button(self, clicked_btn):
		clicked_btn.config(text=self._game.current_player.label)
		clicked_btn.config(fg=self._game.current_player.color)

	""" 게임 디스플레이에 지정된 색상으로 메시지를 출력합니다. """
	def update_display(self, msg, color="black"):
		self.display["text"] = msg
		self.display["fg"] = color

	""" 승자의 승리조건에 해당되는 버튼의 테두리 색을 빨간색으로 보여줍니다. """
	def _highlight_cells(self):
		for button, coordinates in self._cells.items():
			if coordinates in self._game.winner_combo:
				button.config(highlightbackground="red")

	""" 게임 재시작을 위해 보드를 초기화 합니다. """
	def reset_board(self):
		self._game.reset_game()
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
