import socket as sock
import time as t
import CryptoService

host_address = "127.0.0.1"
adress_A = "127.0.0.2"
adress_B = "127.0.0.3"
port = 5500
password3 = b"MySmallPassword3"


def get_key_from_KM(operating_mode):
    # send to KM
    socket = sock.socket()
    socket.bind((adress_A, port + 1))
    socket.connect((host_address, port))
    socket.send(operating_mode)

    # receive key
    response = socket.recv(1024)
    nonce = socket.recv(1024)
    length = socket.recv(10)
    socket.close()
    return response, nonce, "127"

def send_text(message, nonce, length, port): #function for sending code to clientB
    hostname = sock.gethostname()
    socket = sock.socket()
    socket.connect((hostname, port))
    socket.send(message)
    data = socket.recv(1024).decode()
    socket.send(nonce)
    data = socket.recv(1024).decode()
    socket.send(str(length).encode())
    data = socket.recv(1024).decode()

def run():
    print("Enter encryption type?")
    while True:
        type = int(input("1.ECB\n2.CBC\n"))
        if type in (1, 2):
            break
        else:
            print("press 1 or 2")

    if type == 1:
        response, nonce, length = get_key_from_KM(b"ECB")
    else:
        response, nonce, length = get_key_from_KM(b"CBC")

    # connect to client2
    socket = sock.socket()
    socket.bind((adress_A, port))
    socket.connect((adress_B, port))

    if type == 1:
        socket.send(b"ECB")
    else:
        socket.send(b"CBC")

    print(response)
    print(nonce)
    print(length)
    key = CryptoService.decrypt_ECB(response, password3, nonce, int(length))

    print(f"I now possess the key: {key}")
    if socket.recv(1024) == b"Ready to communicate":
        file = open("text.txt", "r")  # read the file
        message = file.read()
        if type == 1:
            info, nonce, length = CryptoService.encrypt_ECB(message, key.encode())
        else:
            info, nonce, length = CryptoService.encrypt_CBC(message, key.encode(), CryptoService.vector)
        send_text(info, nonce, length, 5000)
    print("text sent, job done")


run()
