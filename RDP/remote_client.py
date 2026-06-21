import socket
import threading
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button

def create_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8080))
    print("Connected to server")
    return client


def handle_keyboard(keyboard, data):
    for char in data:
        if char.isprintable():   # avoid garbage
            keyboard.press(char)
            keyboard.release(char)


def handle_mouse(mouse, data):
    try:
        parts = data.strip().split()
        msg_type = parts[0]

        if msg_type == "move":
            x = int(parts[1])
            y = int(parts[2])
            mouse.position = (x, y)

        elif msg_type == "click":
            coords = data.split(',')
            x = int(coords[1])
            y = int(coords[2])
            mouse.position = (x, y)
            mouse.click(Button.left)

        elif msg_type == "scroll":
            print(f"Scroll: {data}")
    except:
        pass  # silently ignore bad parses


def listen_for_commands(client_socket):
    keyboard = KeyboardController()
    mouse = MouseController()
    buffer = ""

    while True:
        raw = client_socket.recv(4096).decode('utf-8', errors='ignore')
        if not raw:
            print("Server disconnected")
            break

        buffer += raw

        while True:
            if buffer.startswith("move "):
                end = buffer.find("move ", 5)
                if end == -1:
                    end = len(buffer)
                msg = buffer[:end].strip()
                if msg:
                    print(f"Received: {msg}")
                    handle_mouse(mouse, msg)
                buffer = buffer[end:].lstrip()

            elif buffer.startswith("click,"):
                end = buffer.find("click,", 6)
                if end == -1:
                    end = len(buffer)
                msg = buffer[:end].strip()
                if msg:
                    print(f"Received: {msg}")
                    handle_mouse(mouse, msg)
                buffer = buffer[end:].lstrip()

            elif buffer.startswith("scroll,"):
                end = buffer.find("scroll,", 7)
                if end == -1:
                    end = len(buffer)
                msg = buffer[:end].strip()
                if msg:
                    print(f"Received: {msg}")
                    handle_mouse(mouse, msg)
                buffer = buffer[end:].lstrip()

            else:
                i = 0
                while i < len(buffer) and not buffer[i:].startswith(("move ", "click,", "scroll,")):
                    i += 1
                if i > 0:
                    msg = buffer[:i]
                    print(f"Received keys: {msg}")
                    handle_keyboard(keyboard, msg)
                    buffer = buffer[i:]
                else:
                    break  

        if len(buffer) > 10240:
            buffer = buffer[-1024:]


if __name__ == "__main__":
    client_socket = create_client()
    
    listener_thread = threading.Thread(target=listen_for_commands, args=(client_socket,), daemon=True)
    listener_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Client shutting down...")
        client_socket.close()