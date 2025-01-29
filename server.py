# SERVER SIDE CODE

import socket
import threading


class ChatServer:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((self.host,self.port))
        self.server.listen()
        # array of connected clients (socket objects)
        self.clients=[]

    def broadcast(self,message,sender):
        for client in self.clients:
            if client != sender:
                client.send(message.encode('utf-8'))

    # what to do when message is received from a client
    def handleClient(self,client):
        while True:
            message=client.recv(1024).decode('utf-8')
            # if message received, send (broadcast) to all other users
            self.broadcast(message,client)

    def run(self):
        while True:
            print('Server is running...')
            # hold until connection is requested to server
            client,address=self.server.accept()
            # add new client to clients list
            self.clients.append(client)
            print('New connection established')

            thread=threading.Thread(target=self.handleClient,args=(client,),daemon=True)
            thread.start()

if __name__=='__main__':
    # Change to local IP address of server
    server=ChatServer('192.168.0.233',55555)
    server.run()
            
