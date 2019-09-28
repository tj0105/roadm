from  threading import  Thread
from socket import *
HOST = "192.168.109.229"
PORT = 20190
BUFSIZE = 1024
ADDR = (HOST, PORT)


def sendMsg(ClientSock):
    while True:
        msg=input(">")
        ClientSock.send(msg.encode("utf-8"))

def recvMsg(ClientSock):
    while True:
        msg=ClientSock.recv(BUFSIZE)
        print("msg:",msg.decode('utf-8'))

def main():
    clientscok=socket(AF_INET,SOCK_STREAM)
    clientscok.connect(ADDR)
    tr=Thread(target=recvMsg,args=(clientscok,))
    ts=Thread(target=sendMsg,args=(clientscok,))


    tr.start()
    ts.start()
if __name__=='__main__':
    main()