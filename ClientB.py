import socket as sock
import time as t
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
    socket.bind((adress_B, port + 2))
    socket.connect((host_address, port))
    socket.send(operating_mode)
    # receive key
    response = socket.recv(2024)
    nonce = socket.recv(1024)
    length = socket.recv(10)
    socket.close()
    return response, nonce, 127


def receive_text(key, type):
    hostname = sock.gethostname()
    port = 5000
    socket = sock.socket()
    socket.bind((hostname, port))

    socket.listen(2)
    conn, address = socket.accept()
    print("Receiving message from: " + str(address))

    message = conn.recv(5000)
    conn.send(b"ack")
    nonce = conn.recv(1024)
    conn.send(b"ack")
    length = conn.recv(1024).decode()
    conn.send(b"ack")

    if type == b'ECB':
        decrypted_message = CryptoService.decrypt_ECB(message, key, nonce, int(length))
    if type == b'CBC':
        decrypted_message = CryptoService.DecryptCBC(message, key, nonce, int(length), CryptoService.vector)

    return decrypted_message  # return transmission from clientA


def run():
    # create socket and wait for clientA
    socket = sock.socket()
    socket.bind((adress_B, port))
    socket.listen(2)
    conn, address = socket.accept()  # accept new connection
    print(str(address) + "has established connection")
    t.sleep(1)
    type = conn.recv(1024)
    if type == b"ECB":
        response, nonce, length = get_key_from_KM(b"ECB")
    else:
        response, nonce, length = get_key_from_KM(b"CBC")

    key = CryptoService.decrypt_ECB(response, password3, nonce, int(length))
    print(f"I now possess the key: {key}")
    # key is now available. Send "ready" to clientA
    conn.send(b"Ready to communicate")
    print(receive_text(key.encode(), type))


run()
