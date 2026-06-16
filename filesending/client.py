import socket



def send_file(file_name,mySocket):
    with open(file_name, "rb") as file:
        data = file.read(1024)
        while data:
            mySocket.send(data)
            data = file.read(1024)
        mySocket.send(b"DONE")
        

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.connect(("127.0.0.1", 8090))

file_name = input("enter the file name\n")
send_file(file_name, mySocket)
mySocket.send(message.encode())
mySocket.close()

