import socket as sock
import time as t

import CryptoService

host_address = "127.0.0.1"
adress_A = "127.0.0.2"
adress_B = "127.0.0.3"
port = 5500


def KM(password1="MySmallPassword1", password2="MySmallPassword2", password3=b"MySmallPassword3"):
    # initiate socket
    socket = sock.socket()  # get instance
    socket.bind((host_address, port))

    # start listening on socket
    socket.listen(100)
    print(f"listening on {host_address}:{port}")
    while True:
        handle_request(socket, password1, password2, password3)
    conn.close()


def handle_request(socket, password1, password2, password3):
    conn, address = socket.accept()  # accept new connection
    print(str(address) + "has just connected")

    # decode data. Maximum 1024 Bytes
    data = conn.recv(1024).decode()
    print(f"from connected user: {data}")

    if data not in ("ECB", "CBC"):
        print("bad request. Closing")
        response = "Bad request"
        conn.send(response.encode())  # send data to the client
    else:
        if data == "ECB":
            response, nonce, length = CryptoService.encrypt_ECB(password1, password3)  # encrypt password1 using password3

        if data == 'CBC':
            response, nonce, length = CryptoService.encrypt_ECB(password2, password3)  # idem

        # send data
        conn.send(response)
        t.sleep(0.1)
        conn.send(nonce)
        t.sleep(0.1)
        conn.send(str(length).encode())
        print(f"The message was sent {response}\n, {nonce}\n, {str(length).encode()}")
    conn.close()

KM()
