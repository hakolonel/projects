import socket


def receive_file(socket, destination):
    with open(destination, "wb") as main_file:
        print("receiving file...")
        chunk = socket.recv(1024)
        while chunk: 
            if b"DONE" in chunk:
                main_file.write(chunk.replace(b"DONE", b""))
                break  
            main_file.write(chunk)
            chunk = socket.recv(1024)


mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "127.0.0.1"
port = 8090
mySocket.bind((ip, port))
mySocket.listen(2)
print("listening on port ", port)
connection, address = mySocket.accept()
receive_file(connection, "received_file.txt")

connection.close()
mySocket.close()
