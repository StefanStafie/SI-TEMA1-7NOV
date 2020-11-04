import socket as sock
import time as t

import CryptoService


def server(password1="MySmallPassword1", password2="MySmallPassword2", password3=b"MySmallPassword3"):
    # initiate socket
    socket = sock.socket()  # get instance
    hostname = sock.gethostname()
    port = 5500
    socket.bind((hostname, port))

    #start listening on socket
    socket.listen(2)
    conn, address = socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    # receive data stream. it won't accept data packet greater than 1024 bytes
    data = conn.recv(1024).decode()
    print("from connected user: " + str(data))

    if data not in ("ECB", "CBC"):
        response = "Wrong encryption type"
        conn.send(response.encode())  # send data to the client
        response = "1"
        conn.send(response.encode())  # send data to the client
        return 0
    else:
        if data == "ECB":
            response, nonce, length = CryptoService.Encrypt(password1, password3)
            print(response, nonce, length)
            conn.send(response)
            print("send response")  # send data to the client
            t.sleep(0.5)
            conn.send(nonce)
            print("sent nonce")  # send data to the client
            t.sleep(0.5)
            conn.send(str(length).encode())
            t.sleep(0.5)
            response = "1"
            conn.send(response.encode())  # send data to the client

        if data == 'CBC':
            response, nonce, length = CryptoService.Encrypt(password2, password3)
            print(response, nonce, length)
            conn.send(response)
            print("send response")  # send data to the client
            t.sleep(0.5)
            conn.send(nonce)
            print("sent nonce")  # send data to the client
            t.sleep(0.5)
            conn.send(str(length).encode())
            t.sleep(0.5)
            response = "1"
            conn.send(response.encode())  # send data to the client
    # conn.close()


def Cryptostart():
    while True:
        server()


Cryptostart()
