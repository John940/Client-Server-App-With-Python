# This server-client project made for python class as Homework
import socket
import threading
import tkinter
from tkinter import *

win = Tk()
win.geometry("680x480")

host = socket.gethostname()  # the ΙP of localhost
port = 5000 

client_socket = socket.socket()  # creating a socket
try:
    client_socket.connect((host, port))  # connect to socket 
except ConnectionRefusedError as error1:
    print(error1)
    print("Problem connection at..", host, port)
    exit()


def receive_msg(client_socket):
    while True:
        data = client_socket.recv(100).decode()  # Waiting for Server Response
        if data.startswith("SERVER RESPONSE"):    # When Server sends the usernames from dictionary
            data = data.lstrip("SERVER RESPONSE dict_keys([")    # we're waiting a dict_keys in a string form response
            data = data.rstrip(")]")    # parsing
            data = data.replace("\'", "")
            data = data.split(",")    # convert string to list
            om1 = OptionMenu(win, options, *data)   # At  option menu button we add the list with usernames
            om1.grid(row=7, column=3)
            continue   
        else:
            if data == "You have left the chat \n":    # If server sends that
                client_socket.close()    
                screen.insert(INSERT, data + "\n")    # Writing the data on screen
                break    # the function and the thread closing
            screen.insert(INSERT, data + "\n")    # Writing the data at screen


def send_msg(client_socket1, message):
    try:
        if message == "":    # MSG TO ALL
            message = writer.get(1.0, "end-1c")  # Gets the string from text area
            message = "SEND MSG " + str(message) + "TO ALL"    # We make the message to the right form for the server
            client_socket1.send(message.encode())
        elif message == "JOIN":
            message = "JOIN" + writer.get(1.0, "end-1c")
            client_socket1.send(message.encode())
        elif message == "special user":    # SND MSG TO 1 USER
            message = "SEND MSG " + writer.get(1.0, "end-1c") + " keyname:" + str(options.get().strip())  # We add keyname word ,so we know that after keyname is the username
            client_socket1.send(message.encode())
        else:
            client_socket1.send(message.encode())
    except OSError as error2:
        screen.insert(INSERT, "You have disconnected" + "\n")
        print("User is disconnected")


options = StringVar(win)
options.set("select user")   # Default option button value
screen = Text(win, height=10, width=60)    # The screen area
writer = Text(win, height=3, width=60)    # The text Area
Button_join = tkinter.Button(win, text="join", command=lambda: send_msg(client_socket, "JOIN"), width="10", height="1")
Button_leave = tkinter.Button(win, text="leave", command=lambda: send_msg(client_socket, "LEAVE"), width="10", height="1")
Button_toall = tkinter.Button(win, text="TO ALL", command=lambda: send_msg(client_socket, ""), width="10", height="1")
Button_touser = tkinter.Button(win, text="To user", command=lambda: send_msg(client_socket, "special user"), width="10", height="1")
screen.grid(row=1, columnspan=4)
writer.grid(row=2, columnspan=3)
Button_join.grid(row=3, column=3)
Button_leave.grid(row=4, column=3)
Button_toall.grid(row=5, column=3)
Button_touser.grid(row=6, column=3)

if __name__ == '__main__':
    threading.Thread(target=receive_msg, args=(client_socket,)).start()    # Starting receive_msg function in a new thread
    print("started thread")
win.mainloop()
