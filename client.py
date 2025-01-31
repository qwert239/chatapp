# CLIENT SIDE CODE

import tkinter as tk
import socket
import threading
import random
import sys

class ChatApplication:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        # chat interface setup
        self.master=tk.Tk()
        self.master.geometry("500x500")
        self.master.title("Chat")
        self.userid=random.randint(1000,9999)

        self.label1=tk.Label(self.master, text="Chat")
        self.label1.pack(pady=10)

        # text box for displaying messages sent
        self.chatDisplay=tk.Text(self.master,width=50)
        self.chatDisplay.pack(pady=10)
        self.chatDisplay.config(state='disabled')

        # text box for message to be sent
        self.entry=tk.Entry(self.master,width=50)
        self.entry.pack(pady=10)

        # send button
        self.sendButton=tk.Button(self.master, text="Send", command=self.sendMessage)
        self.sendButton.pack(padx=10, pady=5)


        self.clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.clientSocket.connect((self.host,self.port))
        except Exception as e:
            print(f"Connection error: {e}")

        self.receiveThread=threading.Thread(target=self.receiveMessage, daemon=True)
        self.receiveThread.start()

        self.master.mainloop()

       


    def sendMessage(self):
        # display message to Text box
        message=self.entry.get()
        # do not display if entry box is empty
        if message=='':
            return
        messageToDisplay=f"User {self.userid}: {message}\n"
        self.chatDisplay.config(state='normal')
        self.chatDisplay.insert(tk.END,messageToDisplay)
        self.chatDisplay.config(state='disabled')
        self.entry.delete(0,tk.END)

        # TEST
        print(messageToDisplay)

        # send message to server
        self.clientSocket.send(messageToDisplay.encode('utf-8'))

    def receiveMessage(self):
        while True:
            message=self.clientSocket.recv(1024).decode('utf-8')
            self.chatDisplay.config(state='normal')
            self.chatDisplay.insert(tk.END,message)
            self.chatDisplay.config(state='disabled')

            # TEST
            print(message)
            
if __name__=='__main__':
    app=ChatApplication(sys.argv[1],55555)

