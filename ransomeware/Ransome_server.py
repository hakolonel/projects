import os
import ssl
import socket

def generate_key(ip):
    random_key = os.urandom(32)
    with open(f"C:/Users/Gaming PC/Downloads/Keys/{ip}", 'wb') as key_file:
        key_file.write(random_key)
    return random_key

def read_key(ip):
    with open(f"C:/Users/Gaming PC/Downloads/Keys/{ip}", 'rb') as key_file:
        return key_file.read()   

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1",8080))
server_socket.listen(1)
print("listening")


while True:
    connection,address = server_socket.accept()
    print("found")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    ssl_connection = context.wrap_socket(connection,server_side = True)
    ip,port = ssl_connection.getpeername()
    key = generate_key(ip)
    ssl_connection.sendall(key)
