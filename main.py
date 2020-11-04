import socket
import CryptoService
import time

key1 = "Nice password101"
key2 = "Nice password202"
key3 = b"Nice password303"


def server_program():
    # get the hostname
    nonce = 0
    nonce = CryptoService.Encrypt(key1, key3)

    host = socket.gethostname()
    port = 5500  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
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
            response, nonce, length = CryptoService.Encrypt(key1, key3)
            print(response, nonce, length)
            conn.send(response)
            print("send response")  # send data to the client
            time.sleep(0.5)
            conn.send(nonce)
            print("sent nonce")  # send data to the client
            time.sleep(0.5)
            conn.send(str(length).encode())
            time.sleep(0.5)
            response = "1"
            conn.send(response.encode())  # send data to the client

        if data == 'CBC':
            response, nonce, length = CryptoService.Encrypt(key2, key3)
            print(response, nonce, length)
            conn.send(response)
            print("send response")  # send data to the client
            time.sleep(0.5)
            conn.send(nonce)
            print("sent nonce")  # send data to the client
            time.sleep(0.5)
            conn.send(str(length).encode())
            time.sleep(0.5)
            response = "1"
            conn.send(response.encode())  # send data to the client
    # conn.close()


def Cryptostart():
    while True:
        server_program()


Cryptostart()
