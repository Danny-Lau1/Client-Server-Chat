from hangman_images import images

def choose_to_play(receive_message, server_or_client_user_name, dedicated_socket):
    """
    Collects a response from user if they want to hangman and calls appropriate function based on input.
    Calls
        - accept_hangman()
        - decline_hangman()
    :param receive_message: function used to send messages to the other host
    :param server_or_client_user_name: username of client or server
    :param dedicated_socket: dedicated connection between server and client
    """

    hangman_response = input(f"{server_or_client_user_name} wants to play Hangman. Press '/y' to play or '/n' to cancel: ")
    while hangman_response != '/y' or hangman_response!= '/n':
        if hangman_response == '/y':
            accept_hangman(receive_message, server_or_client_user_name, dedicated_socket)
        elif hangman_response == '/n':
            decline_hangman(receive_message, server_or_client_user_name, dedicated_socket)
        else:
            hangman_response = input("Not a valid response. Please enter either '/y' to play or '/n' to decline hangman:")




def accept_hangman(receive_message, server_or_client_user_name, dedicated_socket):
    """
    Initiates the setup for a game of hangman.
    Calls
        - play_hangman()
        - receive_message()
    :param receive_message: function used to send messages to the other host
    :param server_or_client_user_name: username of client or server
    :param dedicated_socket: dedicated connection between server and client
    """

    # Triggers the other host to set up a new word
    dedicated_socket.send("/y".encode())
    print(server_or_client_user_name, "is choosing a word...")

    # Receiving the word to guess from the other host
    hangman_word = dedicated_socket.recv(2048).decode()

    # a call to play_hangman()
    play_hangman(hangman_word,server_or_client_user_name, dedicated_socket)

    # returning control back to initiator of hangman
    print("---Waiting For Response---")
    incoming_message = dedicated_socket.recv(2048)

    # Handling the initiator quitting right after playing a game
    if incoming_message.decode() == '/q':
        print(server_or_client_user_name, "has ended the connection!")
        quit()
    receive_message(incoming_message, server_or_client_user_name, dedicated_socket)


def decline_hangman(receive_message, server_or_client_user_name, dedicated_socket):
    """
    Declines initiation from host to play hangman.
    Calls
        - receive_message()
    :param receive_message: function used to send messages to the other host
    :param server_or_client_user_name: username of client or server
    :param dedicated_socket: dedicated connection between server and client
    """

    # Tells other host that receiver of initiation does not want to play
    dedicated_socket.send("/n".encode())

    # Receive message here to ensure turn-based messaging

    print("---Waiting For Response---")
    incoming_message = dedicated_socket.recv(2048)

    # Handling the initiator quitting right after declining a game
    if incoming_message.decode() == '/q':
        print(server_or_client_user_name, "has ended the connection!")
        quit()

    receive_message(incoming_message, server_or_client_user_name, dedicated_socket)




def set_hangman_word(server_or_client_user_name, dedicated_socket):
    """
    When initiator of hangman receives a "/y" from other host.
    Used to set a valid word and send that word over to the other host to start guessing it.
    :param server_or_client_user_name: username of client or server
    :param dedicated_socket: dedicated connection between server and client
    """

    valid_word = False
    word_to_guess = ''
    initial_possibility = input(f"{server_or_client_user_name} has agreed to play! \nRules: Please choose a word with only ascii letters\nYour word:")

    # Ensuring the word to guess only uses letters and no spaces nor empty string
    if initial_possibility.isalpha() == True:
        word_to_guess = initial_possibility

    # Keep repeating this process until user enters a valid word
    else:
        while valid_word == False:
            subsequent_possibility = input("Please choose again:")
            if subsequent_possibility.isalpha() == True:
                valid_word = True
                word_to_guess = subsequent_possibility

    # Sending the word over to the other host
    dedicated_socket.send(word_to_guess.encode())

    # While other user is playing
    print("Other user is currently playing...Please wait...")

    # Tells "word-setter" if other host has won or not
    status = dedicated_socket.recv(2048).decode()
    if status == "won":
        print(server_or_client_user_name, "guessed your word and won!")
    else:
        print(server_or_client_user_name,"was not able to guess correctly. You won!")



def play_hangman(hangman_word, server_or_client_user_name, dedicated_socket):
    """
    :param hangman_word: valid word that used for game
    :param server_or_client_user_name: username of client or server
    :param dedicated_socket: dedicated connection between server and client
    :return:
    """

    # Setting up board and intial state of the game
    dotted_lines = "_" * len(hangman_word)
    correct_completion = False
    already_guessed_letters = []
    num_of_tries = 6

    print("Welcome to Hangman!",f"\n{images[num_of_tries]}",f"\nWord to guess: {dotted_lines}")

    while correct_completion == False and num_of_tries > 0:

        guess = input("Please guess a letter: ")
        if len(guess) == 1 and guess.isalpha(): # checking for a valid guess
            if guess in already_guessed_letters:
                print("You already guessed the letter", guess)
            elif guess not in hangman_word:
                print(guess, "is not in the word.")
                num_of_tries -= 1
                already_guessed_letters.append(guess)
            else:
                print("Good job,", guess, "is in the word!")
                already_guessed_letters.append(guess)
                word_as_list = list(dotted_lines)
                indices = [i for i, letter in enumerate(hangman_word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                dotted_lines = "".join(word_as_list)
                if "_" not in dotted_lines:
                    correct_completion = True
        else:
            print("You can only guess 1 letter!")
        print(f"\n{images[num_of_tries]}",f"\nWord to guess: {dotted_lines}")


    if correct_completion == True:
        print("You are so smart! You've won Hangman!")
        dedicated_socket.send("won".encode())
    else:
        print(server_or_client_user_name, "has won. Better luck next time.")
        dedicated_socket.send("lost".encode())






# play_hangman() function adapted from https://www.youtube.com/watch?v=m4nEnsavl6w
# Date: 03/11/2023





