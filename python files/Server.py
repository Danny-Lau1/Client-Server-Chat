# ----Imports----
import socket
import hangman as hm


# ----Variables-----
ip_address = '127.0.0.1' #IP address for localhost
port_number = 2007


def initialize_server_socket(ip_address, port_number):
    """
    Used to initialize the server socket.
    :param ip_address: Uses a hard-coded ip_address
    :param port_number: Uses a hard-coded port_number
    """

    print("Welcome to the Chat Server")

    # Enter a username so client knows who they are talking to
    server_user_name = input("Please type your username for this session:")

    # Creates a server socket. AF_INET means underlying network is IPv4. SOCK_STREAM indicates it is a TCP socket. ********
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # The bind() method takes an IP address and a port number and binds the socket to this address.
    server_socket.bind((ip_address, port_number))

    # Call to connect with client
    connect_to_client(server_socket, port_number, server_user_name)

def connect_to_client(server_socket, port_number, server_user_name):
    """
    Used to listen for incoming connections from potential clients.
    Creates a dedicated connection with any client that 'knocks' on the door - TCP connection
    :param server_socket: newly created server socket
    :param port_number: Uses a hard-coded port_number
    :param server_user_name: User inputs username they would like client to know
    """

    # The listen() method listens for incoming TCP connections from the client
    server_socket.listen(1)

    # A print statement to show that the server is listening
    print("Server listening on localhost on port", port_number)

    # The accept method waits for the client to connect. When it does, a new socket is created that is dedicated to the client
    #addr returns a tuple of (host, port)
    dedicated_socket, addr = server_socket.accept()

    print("Connection has been made with client from address:", addr)

    # Send your server username to client
    dedicated_socket.send(server_user_name.encode())

    # Retrieve the client username and print the username of who you are talking to
    client_user_name = dedicated_socket.recv(2048).decode()
    print(f"You have connected with client host {client_user_name}!")

    print('If you wish to quit this program at anytime, please type "/q"')
    print('If you wish to initiate a game of hangman with the other host, please type "/h"')

    # A call to send or receive messages
    server_send_and_receive_messages(dedicated_socket, client_user_name)

def server_send_and_receive_messages(dedicated_socket, client_user_name):
    """
    A while loop that keeps the connection between server and client alive.
    Calls
        - compose_message()
        - receive_message()
    :param dedicated_socket: dedicated connection between server and client
    :param client_user_name: client's username
    """

    # Keep the connection alive until server enters "/q"
    connected = True
    while connected:
        # Composing a message greater than length 0
        outgoing_message = compose_message()

        # Quitting the program
        if outgoing_message == "/q":
            dedicated_socket.send(outgoing_message.encode())
            break # closes the connection on this side and jumps down to close_connection()

        else:
            dedicated_socket.send(outgoing_message.encode()) # sending of the actual message

        print("---Waiting For Response---")

        # Handling receiving a message
        incoming_message = dedicated_socket.recv(2048)
        connected = receive_message(incoming_message, client_user_name, dedicated_socket)

    close_connection(dedicated_socket)

def compose_message():
    """
    Used to compose a message that has > 0 bytes.
    :return: return an outgoing_message back in server_send_and_receive_message()
    """
    outgoing_message = input("Me:")

    # Make sure that the message is greater than 0 bytes
    while len(outgoing_message) == 0:
        outgoing_message = input("Cannot send an empty message. Please Try Again:")
    return outgoing_message

def receive_message(incoming_message, client_user_name, dedicated_socket):
    """
    Uses imports from hangman.py.
    Checks multiple conditions based on client's message:
        - "/q" - can quit program if message
        - "/h" - can prompt server to choose to play hangman
        - "/y" - can play as the "word setter" if client accepts your initiation to play hangman
        - "/n" - can tell you that client does not want to play when you initiate hangman
        - returns a regular message back to you
    Calls
        - hm.choose_to_play()
        - hm.set_hang_man_word()
    :param incoming_message: the message that is received by the server from the client
    :param client_user_name: client's username
    :param dedicated_socket: dedicated connection between server and client
    :return: returns either True or False back to server_send_and_receive_message() to determine if connection is still alive
    """

    if incoming_message.decode() == "/q":
        print("Client has ended connection!")
        return False # Terminates while loop from above

    elif incoming_message.decode()== "/h":
        # player can make a choice to play. returns true to keep while loop above connected
        hm.choose_to_play(receive_message, client_user_name, dedicated_socket)
        return True

    elif incoming_message.decode() == '/y':
        hm.set_hangman_word(client_user_name, dedicated_socket)
        return True

    elif incoming_message.decode() == "/n":
        print(client_user_name, "does not want to play Hangman at the moment.")
        return True

    else:
       print(f"{client_user_name}: {incoming_message.decode()}")
       return True # Keeps while loop alive

def close_connection(dedicated_socket):
    """
    Closes connection with client.
    :param dedicated_socket: dedicated connection between server and client
    """

    print("Server Socket is closing...Thank You!")
    dedicated_socket.close()

initialize_server_socket(ip_address, port_number)


# Citation for this program uses the resources from:
#-----------------
# Kurose and Ross, Computer Networking: A Top-Down Approach, 8th Edition, Pearson
# Pages 154 - 164
# Date: 03/11/2023
#-----------------
# https://www.youtube.com/watch?v=3QiPPX-KeSc