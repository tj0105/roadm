from socket import *
from time import ctime
import datetime

HOST = "192.168.109.229"
PORT =20192
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
revceive_list=[]
while True:
    print("waiting for connection...")
    tcpCliSock, addr = tcpSerSock.accept()
    print("connected from :", addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)
        print(len(data))
        print(data[len(data)])
        if not data:
            break
        revceive_list=data.split()+revceive_list
        # print(len(revceive_list))
        content = '[%s] %s' % (bytes(ctime(), "utf-8"), data)
        # print(type(data))
        # print(datetime.datetime.now().strftime('%H:%M:%S.%f'))
        # print(data.decode("utf-8"))

        # print(type(data))
        # print(type(content))
        tcpCliSock.send(content.encode("utf-8"))

    tcpCliSock.close()

tcpSerSock.close()

