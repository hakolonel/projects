from pynput.keyboard import Key, Listener
from pynput.mouse import Listener as MouseListener
import socket
import threading

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

def key_thread(client_socket):
    def send_key(key):
        client_socket.send(key.char.encode())
        print(f"Sent key: {key}")
    with Listener(on_press=send_key) as key_listener:
        key_listener.join()


def mouse_thread(client_socket):
    def on_move(x, y):
        message = f"move {x} {y}"
        client_socket.send(message.encode())
        print(f"Mouse moved to: {x}, {y}")
    def on_click(x, y, button, pressed):    
        if pressed:
            message = f"click,{x},{y}"
            client_socket.send(message.encode())
            print(f"Mouse clicked at: {x}, {y} with button {button}")
    def on_scroll(x, y, dx, dy):
        message = f"scroll,{x},{y}"
        client_socket.send(message.encode())
        print(f"Mouse scrolled at: {x}, {y} with delta {dx}, {dy}")
    with MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as mouse_listener:
        mouse_listener.join()





if __name__ == "__main__":
        server_socket = create_server()
        client_socket = accept_connections(server_socket)

        thread1 = threading.Thread(target=key_thread, args=(client_socket,))
        thread1.start()
        thread2 = threading.Thread(target=mouse_thread, args=(client_socket,))
        thread2.start()
        

