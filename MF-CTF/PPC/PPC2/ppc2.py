import socket
import base64
import io
from time import sleep
import pytesseract
from PIL import Image, UnidentifiedImageError

def send_data_back(sock: socket, message: str):
    sock.send((message + '\r\n').encode())


def read_data_from_socket(sock: socket):
    return sock.recv(SIZE*8)


def get_image_from_raw_data(data: bytearray):
    data = data.decode('utf-8')
    result = ''
    start = 0
    end = 0
    for i in range(0, len(data) - 1):
        if data[i] == chr(39) and start == 0:
            start = i
        if data[i] == chr(39) and start > 0:
            end = i
    result = data[start + 1:end]
    return result


def sanitize_text(message: str):
    message.replace("8", "&")
    parts = message.split("&")
    for i in range(0, len(parts)):
        if parts[i][0] == " " or parts[i][0] == "_":
            parts[i] = parts[i][1:]
        if parts[i][len(parts[i]) - 1] == " " or parts[i][len(parts[i]) - 1] == "_":
            parts[i] = parts[i][:-1]
        parts[i] = parts[i].replace(" ", "")
        parts[i] = parts[i].replace("_", "")
        parts[i] = parts[i].replace("_ ", "")
        parts[i] = parts[i].replace(" _", "")
        parts[i] = parts[i].replace("_8", "")
        parts[i] = parts[i].replace("8", "")
        parts[i] = parts[i].replace("8_", "")
        parts[i] = parts[i].replace("._", "")
        parts[i] = parts[i].replace(".", "")
        parts[i] = parts[i].replace(". ", "")
        parts[i] = parts[i].replace(" .", "")
        parts[i] = parts[i].replace("\n", "")
    # parts[0] = speller.correction(parts[0])
    # parts[1] = speller.correction(parts[1])
    # parts[2] = speller.correction(parts[2])
    print(parts)
    return parts[0] + "_&_" + parts[1] + "_&_" + parts[2]


pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
URL = '195.50.2.219'
PORT = 9007
SIZE = 1024
SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCK.connect((URL, PORT))

COUNTER = 250
try:
    while COUNTER != 0:
        buffer = read_data_from_socket(SOCK)
        print(buffer.decode())
        buffer = get_image_from_raw_data(buffer)
        # print(buffer)
        b_decoded = base64.b64decode(buffer)
        # print(b_decoded)
        img = Image.open(io.BytesIO(b_decoded))
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(img, lang='eng', config=custom_config)
        # text = text.replace("_&", "_&_")
        # text = text.replace("_&__", "_&_")
        print(text)
        text = text[:len(text) - 1]
        text = sanitize_text(text)
        print(text)
        send_data_back(SOCK, text)
        sleep(0.2)
        COUNTER -= 1
except UnidentifiedImageError as error:
    print("Exception: " + str(error))
finally:
    print(read_data_from_socket(SOCK))
    SOCK.close()
