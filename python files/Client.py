# ----Imports----
import socket
import hangman as hm


# ----Variables-----
ip_address = '127.0.0.1'
port_number = 2007

def initialize_client_server(ip_address, port_number):
    """
    Used to initialize the client socket.
    :param ip_address: Uses a hard-coded ip_address
    :param port_number: Uses a hard-coded port_number
    """

    print("Welcome to the Chat Server")

    # Create a username so server knows who they are talking to
    client_user_name = input("Please type your username for this session:")

    # Creates a client socket. AF_INET means underlying network is IPv4. SOCK_STREAM indicates it is a TCP socket.
    dedicated_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Call to connect with client
    connect_to_server(dedicated_socket, client_user_name)

def connect_to_server(dedicated_socket, client_user_name):
    """
    Used to connect with a server that is listening on a specific ip_address and port_number.
    :param dedicated_socket: dedicated connection between server and client
    :param client_user_name: User inputs username that would like server to know
    """

    # Client connects with listening socket
    dedicated_socket.connect((ip_address, port_number))

    # client sends their username to server
    dedicated_socket.send(client_user_name.encode())

    # Receiving the server username
    server_user_name = dedicated_socket.recv(2048).decode()

    print(f"You have connected with servr host {server_user_name}!")
    print('If you wish to quit this program at anytime, please type "/q"')
    print('If you wish to initiate a game of hangman with the other host, please type "/h"')
    print("---Waiting For Initial Message---")

    # Server is to make initial message to client. Client is put in receiving mode when connection is made
    incoming_message = dedicated_socket.recv(2048)

    # Handling receiving a message. Also handles server quitting upon first message to client
    connected= receive_message(incoming_message, server_user_name, dedicated_socket)
    client_send_and_receive_messages(dedicated_socket, server_user_name, connected)


def client_send_and_receive_messages(dedicated_socket, server_user_name, connected = True):
    """
    A while loop that keeps the connection between server and client alive.
    Calls compose_message(), receive_message()
    :param dedicated_socket: dedicated connection between server and client
    :param server_user_name: server's username
    :param connected: A boolean that keeps the while  loop and chat exchange going
    """

    # Keep the connection alive until client enters "/q"
    while connected:
        # Composing a message greater than length 0
        outgoing_message = compose_message()

        # Quitting the program
        if outgoing_message == "/q":
            dedicated_socket.send(outgoing_message.encode())
            break #closes the connection on this side and jumps down to close_connection()

        else:
            dedicated_socket.send(outgoing_message.encode())

        print("---Waiting For Response---")

        # Handling receiving a message
        incoming_message = dedicated_socket.recv(2048)
        connected = receive_message(incoming_message, server_user_name, dedicated_socket)


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

def receive_message(incoming_message, server_user_name, dedicated_socket):
    """
    Uses imports from hangman.py.
    Checks multiple conditions based on client's message:
        - "/q" - can quit program if message
        - "/h" - can prompt client to choose to play hangman
        - "/y" - can play as the "word setter" if server accepts your initiation to play hangman
        - "/n" - can tell you that server does not want to play when you initiate hangman
        - returns a regular message back to you
    Calls
        - hm.choose_to_play()
        - hm.set_hang_man_word()
    :param incoming_message: the message that is received by the server from the client
    :param client_user_name: client's username
    :param dedicated_socket: dedicated connection between server and client
    :return: returns either True or False back to server_send_and_receive_message() to determine if connection is still alive
    """
    # When the client receives "/q" from the server
    if incoming_message.decode() == "/q":
        print("Server has ended connection!")
        return False # Terminates while loop from above

    elif incoming_message.decode()== "/h":
        # player can make a choice to play. returns true to keep while loop above connected
        hm.choose_to_play(receive_message, server_user_name, dedicated_socket)
        return True

    elif incoming_message.decode() =='/y': ############
        hm.set_hangman_word(server_user_name, dedicated_socket)
        return True


    elif incoming_message.decode() == "/n":
        print(server_user_name, "does not want to play Hangman at the moment.")
        return True

    else:
        print(f"{server_user_name}: {incoming_message.decode()}")
        return True # Keeps while loop alive

def close_connection(dedicated_socket):
    """
    Closes connection with client.
    :param dedicated_socket: dedicated connection between server and client
    """

    print("Client Socket is closing...Thank You!")
    dedicated_socket.close()

initialize_client_server(ip_address, port_number)

# Citation for this program uses the resources from:
#-----------------
# Kurose and Ross, Computer Networking: A Top-Down Approach, 8th Edition, Pearson
# Pages 154 - 164
# Date: 03/11/2023
#-----------------
# https://www.youtube.com/watch?v=3QiPPX-KeSc
