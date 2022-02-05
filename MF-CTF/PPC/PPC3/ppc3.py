import socket
import re


def binary_search(array, x, lower=0, higher=None):
    if lower < 0:
        raise ValueError('Должен быть положительным!')
    if higher is None:
        higher = len(array)
    while lower < higher:
        middle = (lower + higher) // 2
        if array[middle] < x:
            lower = middle + 1
        else:
            higher = middle
    return lower


URL = '195.50.2.219'
PORT = 9008
SIZE = 1024
SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCK.connect((URL, PORT))
YES = 'да'.encode('utf-8')
NO = 'нет'.encode('utf-8')
data = SOCK.recv(SIZE).decode('utf-8')
print(data)
data_lines = data.split('\n')
info = re.findall(r"\d+", data_lines[-3])
print(info)
secret = 512
for x in range(0, int(info[0])):
    secret = 0
    value = int(info[2]) / 2
    SOCK.send(("<" + str(value) + '\r\n').encode('utf-8'))
    answer = SOCK.recv(SIZE).decode('utf-8')
    print(answer)
    if answer == YES:
        print("[!]: secret is less then " + value)
        value = value / 2
    if answer == NO:
        print("[!]: secret is larger then " + value)
        value = value + (value / 2)
    if x == int(info[0]) - 1 and answer == YES:
        secret = value

print(secret)
