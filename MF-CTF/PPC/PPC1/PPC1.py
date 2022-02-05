import socket
import math
from time import sleep
import re


def parse_data(data):
    buf_len = len(data)
    values = ""
    # read data from the end to find all 4 digits
    for x in range(2, buf_len - 1):
        if str(data[-x]) == '10':
            break
        values += chr(data[-x])
    values = values[::-1]
    return values


def distance(points_coefs: list):
    return math.sqrt(math.pow(points_coefs[2] - points_coefs[0], 2)
                     + math.pow(points_coefs[3] - points_coefs[1], 2))


# trying to connect to MF-CTF
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('ctf.mf.grsu.by', 9002))
counter = 0
flag_found = 0
while counter <= 50:
    print("Step: " + str(counter))
    sleep(1)
    if counter == 50:
        data = s.recv(1024).decode('utf-8')
        if 'grodno{' in data:
            print("[+] flag: " + (re.findall(r"grodno{.+?}", data))[0])
            flag_found = 1
            break
    data = s.recv(1024)
    print(data.decode('utf-8'))
    # coord in the end (format: x1,y1 -> x2,y2)
    if flag_found != 1:
        values = parse_data(data)
        points_coefs = [int(x) for x in values.split(';')]
        print(points_coefs)
        d = distance(points_coefs)
        d = round(d, 2)
        print(d)
        s.send((str(d) + '\r\n').encode())
    counter += 1
s.close()
