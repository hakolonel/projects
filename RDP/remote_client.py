import socket
from pynput.keyboard import Controller, Key

def create_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8080))
    print("Connected to server")
    return client


client_socket = create_client()
keyboard = Controller()

while True:
    key = client_socket.recv(1024).decode()
    keyboard.press(key)
