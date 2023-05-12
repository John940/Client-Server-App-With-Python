# This server-client project made for python class as Homework
import socket
import threading
customers = {}    # dictionary with key = username, value = connections


def do_thejob(conn):
    while True:
        try:
            data = conn.recv(1024).decode()  # waiting the client response..
            print(data, "I RECEIVED")
        except ConnectionAbortedError:
            print("Connection lost it from client..")
            conn.close()
            break
        if data.startswith("JOIN"):    
            conn.send("Please insert a username and press JOIN Button".encode())    # Asking for username..
            username = conn.recv(1024).decode()    # waiting client response..
            while username.startswith("JOIN") is False or username == "JOIN":   
                conn.send("Please insert a username and press JOIN Button".encode())
                username = conn.recv(1024).decode()
            username = username.lstrip("JOIN")    # parsing the response
            customers[username] = conn    # add the client response to customers list
            conn.send("welcome to chat room ".encode() + username.encode())
            update_the_user_list()
            while data != "LEAVE":    # While user don't send leave...Listen for the response
                data = conn.recv(1024).decode()
                if not data:
                    continue
                elif data == "LEAVE":    # If user wants leave
                    conn.send("You have left the chat \n".encode())
                    customers.pop(username)    # delete the user from customers dictionary
                    update_the_user_list()
                elif data.startswith("SEND MSG") and data.endswith("TO ALL"):   # If messaging TO ALL
                    print("from connected user: " + str(data))
                    for customer in customers:   
                        try:
                            data = str(data).lstrip("SEND MSG")   # parsing
                            data = str(data).rstrip("TO ALL")
                            customers[customer].send(data.encode())   # Send the message    
                        except:
                            print("error on deliver at", customers[customer])
                    conn.send("message delivered".encode())   # Report of success delivery
                elif data.startswith("SEND MSG") and data[data.find("keyname:") + 8:] in customers.keys():    # If last word from message is in  dict_keys()
                    data = str(data).lstrip("SEND MSG")    # parsing
                    customers[data[data.find("keyname:") + 8:]].send(data[: data.find("keyname:")-1].encode())    # Send the message to user without last words
                    print("message delivered to" + data[data.find("keyname:") + 8:])
                    conn.send("message delivered".encode())   # Report of success delivery
                else:
                    conn.send("I dont know where to send your message ...try again \n".encode())    # If message have bad form
                    print("i dont recognize,", data)
        else:
            try:
                conn.send("if you wanna join, you must enter JOIN".encode())    # While user don't press JOIN
            except ConnectionAbortedError:
                print("Connection lost from client...")
                conn.close()
                break


def update_the_user_list():   
    print("i started the update...")
    for connection in customers.values():
        connection.send("SERVER RESPONSE".encode() + str(customers.keys()).encode())    # Sending the usernames from dictionary
    print("i update it")


def server_program():
    while True:  
        host = socket.gethostname()   # the IP of localhost
        port = 5000
        server_socket = socket.socket()  
        server_socket.bind((host, port)) 

        server_socket.listen(2)   # we re listening for 2 connections
        conn, address = server_socket.accept()  # accept connection...
        print("Connection from: " + str(address))
        threading.Thread(target=do_thejob, args=(conn,)).start()    # starting the do_thejob function in a new thread...with conn as argument
        print("new thread started...")


if __name__ == '__main__':
    server_program()
