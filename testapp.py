import socket
import sys
from threading import Thread
from time import sleep
from pprint import pprint as pprint

listenPort=80
packetNum=1

def client_thread(clientSock):
    global packetNum

    print("connection from " + str(clientSock.getpeername()))
    message = "{0}:{1} #{2}\n".format(socket.gethostname(),listenPort,packetNum)
    packetNum+=1

    msg = message.encode('utf-8')
    totalsent = 0
    while totalsent < len(msg):
        sent = clientSock.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

    clientSock.close()

def beClient(ip,port):
    print("Connecting to {0}:{1}".format(ip,port))
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((ip,int(port)))
    data = clientsocket.recv(1000)
    pprint(data)
    clientsocket.close()

def main():
    print("TestApp V1\n")
    #create an INET, STREAMing socket
    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    #bind the socket to a public host,
    # and a well-known port
    str = socket.gethostname()
    serversocket.bind(('0.0.0.0', listenPort))
    #become a server socket
    serversocket.listen(5)

    print("Container " + socket.gethostname() + " listening for Clients....")
    pprint(serversocket.getsockname())

    while True:
        #accept connections from outside
        (clientsocket, address) = serversocket.accept()
        #now do something with the clientsocket
        #in this case, we'll pretend this is a threaded server
        ct = Thread(target= client_thread,args=(clientsocket,))
        ct.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        beClient(sys.argv[1],sys.argv[2])
    else:
        main()
