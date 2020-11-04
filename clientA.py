import socket
import time
import CryptoService
import EncryptedTalk

key3 = b"Nice password303"


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
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
            response = "The encryption type will be: " + data
            conn.send(response.encode())  # send data to the client
            response = "1"
            conn.send(response.encode())  # send data to the client
            conn.close()
            return data


def client_program(message, port):
    host = socket.gethostname()  # as both code is running on same pc
    working = True

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    client_socket.send(message.encode())
    response = []
    while working:
        # send message

        data = client_socket.recv(1024)  # receive response

        # print('Received from server: ' + data)  # show in terminal
        try:
            data = data.decode()

            data1 = int(data)
            if data1 == 1:
                working = False
                break

        except:
            pass
        response.append(data)
    # client_socket.close()  # close the connection

    return response


# client_program()

def Service1():
    file = open("Message.txt", "r")
    mess = file.read()

    print("What type of encryption do you want?")
    try:
        type = int(input("1.ECB\n2.CBC\n"))
        if type not in (1, 2):
            print("Wrong input")
            quit(0)
    except:
        print("Wrong input")
        quit(0)
    if type == 1:
        client_program("ECB", 5000)
        info = client_program("ECB", 5500)
        key = CryptoService.Decrypt(info[0], key3, info[1], int(info[2]))
    else:
        client_program('CBC', 5000)
        info = client_program("CBC", 5500)
        key = CryptoService.Decrypt(info[0], key3, info[1], int(info[2]))
    types = server_program()

    if types == "ECB":
        text, nonce, length = CryptoService.Encrypt(mess, key.encode())
        EncryptedTalk.client_encoded(text, nonce, length, 5000)
    if types == "CBC":
        text, nonce, length = CryptoService.EncryptCBC(mess, key.encode(), CryptoService.vector)

        EncryptedTalk.client_encoded(text, nonce, length, 5000)


Service1()


def Test():
    message = input('PUT YOUR MEESAGE')
    encryptType = 'CBC'
    if encryptType == 'ECB':
        text, nonce, length = CryptoService.Encrypt(message, b"Nice password101")
        EncryptedTalk.client_encoded(text, nonce, length, 5000)
    if encryptType == 'CBC':
        text, nonce, length = CryptoService.EncryptCBC(message, "Nice password101".encode(), CryptoService.vector)
        # print(text)
        EncryptedTalk.client_encoded(text, nonce, length, 5000)

# Test()
