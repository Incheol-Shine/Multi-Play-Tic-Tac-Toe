import socket
from threading import *
from time import sleep

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while (1):
    print("send message : ", end = '')
    message = input() + '\0'
    client_socket.send(message.encode())
    sleep(1)

client_socket.close()