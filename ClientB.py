import socket as sock
import time as t
import EncryptedTalk
import CryptoService

password3 = "MySmallPassword3"

host_address = "127.0.0.1"
adress_A = "127.0.0.2"
adress_B = "127.0.0.3"
port = 5500
password3 = b"MySmallPassword3"


def get_key_from_KM(operating_mode):
    # send to KM
    socket = sock.socket()
    socket.bind((adress_B, port))
    socket.connect((host_address, port))
    socket.send(operating_mode)

    t.sleep(1)  # wait for message to be written to socket
    response = socket.recv(1024)  # receive key
    nonce = socket.recv(1024)
    length = socket.recv(1024)
    socket.close()
    return response, nonce, length


def run():
    # create socket and wait for clientA
    socket = sock.socket()
    socket.bind((adress_B, port))
    socket.listen(2)
    conn, address = socket.accept()  # accept new connection
    print(str(address) + "has established connection")

    if type == 1:
        response, nonce, length = get_key_from_KM(b"ECB")
        socket.send("ECB")
    else:
        response, nonce, length = get_key_from_KM(b"CBC")
        socket.send("CBC")

    key = CryptoService.Decrypt(response, password3, nonce, int(length))

    t.sleep(1)
    if socket.recv(1024) == "Ready to communicate":
        file = open("Message.txt", "r")  # read the file
        for message in file.read():
            if type == 1:
                text, nonce, length = CryptoService.Encrypt(message, key.encode())
            else:
                text, nonce, length = CryptoService.EncryptCBC(message, key.encode(), CryptoService.vector)
            socket.send(bytes(message))
        socket.send(b"Transmission ended.")


run()
