from socket import *

HOST = "192.168.109.229"
PORT = 20192
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    data = input("> ")
    if not data:
        break

    tcpCliSock.send(data.encode("utf8"))
    data = tcpCliSock.recv(BUFSIZ)
    print(data.decode("utf-8"))

tcpCliSock.close()
