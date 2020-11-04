from Crypto.Cipher import AES

vector = '11001100010010111001110101001011000101001111000001010001111001000110000100100111000001110011011011010100100011111110100101101010'


def Encrypt(message, key):
    temp = message.encode('UTF-8')

    binform = bin(int(temp.hex(), 16))[2:]  ##.zfill doesn't work !?!?!?!
    initialLength = len(binform)
    # print(binform)
    for i in range(0, 128 - len(binform) % 128):
        binform += '0'

    cypher = AES.new(key, AES.MODE_EAX)
    nonce = cypher.nonce
    cryptotext = b''

    for i in range(0, len(binform), 128):
        sector = binform[0 + i:0 + i + 128]
        cryptotext += (cypher.encrypt(sector.encode('UTF-8')))
    return cryptotext, nonce, initialLength


def Decrypt(message, key, nonce, length):
    cypher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    text = ''

    for i in range(0, len(message), 128):
        text += cypher.decrypt(message[i:i + 128]).decode('UTF-8')

    text = text[0:length]

    text = hex(int(text, 2))[2:]
    truetext = ''
    for i in range(0, len(text), 2):
        truetext += chr(int(text[i:i + 2], 16))
    return truetext


def EncryptCBC(message, key, vector):
    temp = message.encode('UTF-8')

    binform = bin(int(temp.hex(), 16))[2:]  ##.zfill doesn't work !?!?!?!
    initialLength = len(binform)
    for i in range(0, 128 - len(binform) % 128):
        binform += '0'

    cypher = AES.new(key, AES.MODE_EAX)
    nonce = cypher.nonce
    cryptotext = b''
    bullshit = AES.new(key, AES.MODE_EAX, nonce)
    for i in range(0, len(binform), 128):
        sector = binform[0 + i:0 + i + 128]

        #  print(sector)
        sector = bin((int(sector, 2) ^ int(vector, 2)))[2:].zfill(128)
        # print(sector)
        temp = cypher.encrypt(sector.encode('UTF-8'))
        cryptotext += temp
        vector = bullshit.decrypt(temp).decode('UTF-8')
    print()
    return cryptotext, nonce, initialLength


def DecryptCBC(message, key, nonce, length, vector):
    cypher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    text = ''

    for i in range(0, len(message), 128):
        temp = cypher.decrypt(message[i:i + 128]).decode('UTF-8')
        # print(temp)
        temp2 = bin((int(temp, 2) ^ int(vector, 2)))[2:].zfill(128)
        text += temp2
        vector = temp
    #  print(temp)

    text = text[0:length]

    text = hex(int(text, 2))[2:]
    truetext = ''
    for i in range(0, len(text), 2):
        truetext += chr(int(text[i:i + 2], 16))
    return truetext


def testingground():
    text, nonce, length = Encrypt("This need to be a way bigger message", b"Nice password101")
    print(Decrypt(text, b"Nice password101", nonce, length))


# testingground()

def testtingground2():
    text, nonce, length = EncryptCBC('BULLSHIT MEtHOD AND LETS MAKE IT BIGGER', b"Nice password101", vector)
    print(DecryptCBC(text, b"Nice password101", nonce, length, vector))

# testtingground2()
