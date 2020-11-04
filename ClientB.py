import socket
import time
import EncryptedTalk
import CryptoService

password3 = "MySmallPassword3"

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
            # conn.close()
            return data


# conn.close()  # close the connection
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


def MainService():
    type = server_program()
    print(type)
    time.sleep(3)
    info = client_program(type, 5500)
    key = CryptoService.Decrypt(info[0], password3, info[1], int(info[2]))
    client_program(type, 5000)

    EncryptedTalk.server_program(key.encode(), type)


def Test():
    EncryptedTalk.server_program(b"Nice password101", 'CBC')


# Test()
MainService()
