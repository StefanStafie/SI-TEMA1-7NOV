import socket
import CryptoService


def client_encoded(message, nonce, length, port):
    host = socket.gethostname()  # as both code is running on same pc
    working = True

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    client_socket.send(message)
    data = client_socket.recv(1024).decode()
    client_socket.send(nonce)
    data = client_socket.recv(1024).decode()
    client_socket.send(str(length).encode())
    data = client_socket.recv(1024).decode()

    data = client_socket.recv(1024).decode()
    print("message from server:" + data)
    data = client_socket.recv(1024).decode()
    response = 0
    print(data)

    # client_socket.close()  # close the connection
    return response


def server_program(key, encryptType):
    print(encryptType)
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance

    server_socket.bind((host, port))  # bind host address and port together

    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    try:
        message = conn.recv(1024)
        conn.send('1'.encode())
        nonce = conn.recv(1024)
        conn.send('1'.encode())
        length = conn.recv(1024).decode()
        conn.send('1'.encode())

    except:
        print('Something went wrong with data transmission')
        quit(-1)

    try:
        if encryptType == 'ECB':
            decryptedmessage = CryptoService.Decrypt(message, key, nonce, int(length))
            print("message received from client:" + decryptedmessage)
            conn.send('Thanks for the message'.encode())
            conn.send('1'.encode())
        if encryptType == 'CBC':
            decryptedmessage = CryptoService.DecryptCBC(message, key, nonce, int(length), CryptoService.vector)
            print("Message received from client: " + decryptedmessage)
            conn.send('Thanks for the message'.encode())
            conn.send('1'.encode())
    except Exception:
        print(Exception)
        print("something went wrong with the decryption")
        quit(-1)

# TestingGround()
