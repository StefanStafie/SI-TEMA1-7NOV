from Crypto.Cipher import AES

vector = '11110000111100001111000011110000111100001111000011110000111100001111000011110000111100001111000011110000111100001111000011110000'


def encrypt_ECB(message, key):
    # get the message in a workable format
    temp = message.encode('UTF-8')
    bin_format = bin(int(temp.hex(), 16))[2:]
    len_binform = len(bin_format)

    # add zeros padding
    for i in range(0, 128 - len(bin_format) % 128):
        bin_format += '0'

    # use AES
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce  # Does not work without nonce
    # encrypt here. For each sector of 128 bits, DO ENCRYPT
    crypto_text = b''
    for i in range(0, len(bin_format), 128):
        sector = bin_format[0 + i:0 + i + 128]
        crypto_text += (cipher.encrypt(sector.encode('UTF-8')))
    # done
    return crypto_text, nonce, len_binform


def decrypt_ECB(message, key, nonce, length):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    text = ''

    # for each sector of 128 bits, DO DECRYPT
    for i in range(0, len(message), 128):
        text += cipher.decrypt(message[i:i + 128]).decode('UTF-8')

    text = text[0:length]  # Do not get the padding

    text = hex(int(text, 2))[2:]

    # convert back to readable text
    text2 = ''
    for i in range(0, len(text), 2):
        text2 += chr(int(text[i:i + 2], 16))
    return text2


def encrypt_CBC(message, key, vector):
    # prepare message for encoding
    temp = message.encode('UTF-8')
    bin_format = bin(int(temp.hex(), 16))[2:]
    bin_length = len(bin_format)
    # add zeros padding
    for i in range(0, 128 - len(bin_format) % 128):
        bin_format += '0'
    # use AES
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    cryptotext = b''

    # for each sector of 128 bits, DO ENCRYPT
    cipher2 = AES.new(key, AES.MODE_EAX, nonce)
    for i in range(0, len(bin_format), 128):
        sector = bin_format[0 + i:0 + i + 128]
        sector = bin((int(sector, 2) ^ int(vector, 2)))[2:].zfill(128)
        temp = cipher.encrypt(sector.encode('UTF-8'))
        cryptotext += temp
        vector = cipher2.decrypt(temp).decode('UTF-8')
    # done
    return cryptotext, nonce, bin_length


def DecryptCBC(message, key, nonce, length, vector):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    text = ''

    # for each sector of 128 bits, DO DECRYPT
    for i in range(0, len(message), 128):
        temp = cipher.decrypt(message[i:i + 128]).decode('UTF-8')
        temp2 = bin((int(temp, 2) ^ int(vector, 2)))[2:].zfill(128)
        text += temp2
        vector = temp

    # text2 is readable(human language) text
    text = text[0:length]
    text = hex(int(text, 2))[2:]
    text2 = ''

    # decrypt here. For each sector of 128 bits, DO DECRYPT
    for i in range(0, len(text), 2):
        text2 += chr(int(text[i:i + 2], 16))

    return text2


def test_cbc():
    file = open("text.txt", "r")  # read the file
    message = file.read()
    key = b"1234567890123456"  # key
    info, nonce, length = encrypt_CBC(message, key, vector)  # encrypt
    print(DecryptCBC(info, key, nonce, length, vector))  # print(decrypt)


def test_ecb():
    file = open("text.txt", "r")  # read the file
    message = file.read()
    key = b"1234567890123456"  # key
    info, nonce, length = encrypt_ECB(message, key)  # encrypt
    print(decrypt_ECB(info, key, nonce, length))  # print(decrypt)

# test_ecb()
# test_cbc()
