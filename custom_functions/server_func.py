import custom_functions.note as notes
import custom_functions.sql_funcs as sql_funcs
import time
import os

# provides a quick way to clear the screen of a client connection using a 
# simple escape sequence

#Change this to the location of the database
DATABASE_LOCATION = None

def init_server_vars():
    global DATABASE_LOCATION
    DATABASE_LOCATION = os.environ.get('DATABASE_LOCATION')


# ONLY WORKS FOR LINUX
def clear_screen(client_socket):
            clear_screen_command = '\033[2J\033[H' # This escape sequence clears the Linux terminal screen.
            client_socket.send(bytes(clear_screen_command, encoding='utf-8'))

# Prints the main menu for the program
# RETURN CODES:
# ret - the user id of the logged in user IF THEY EXIST AND SUCCESSFULLY LOGGED IN
# -1 - generic ret code (keeps program looping)
# -2 - exit the program

def print_main_menu(cs):
    cs.send("--------MENU----------\n".encode())
    cs.send("1. Login\n".encode())
    cs.send("2. Register\n".encode())
    cs.send("3. Exit\n\n".encode())

    cs.send("Enter your choice: ".encode())
    choice = cs.recv(1024).strip().decode()
    if choice == "1":
        clear_screen(cs)
        ret = login(cs)
        return ret
    elif choice == "2":
        register(cs)
        return -1
    elif choice == "3":
        return -2
    else:
        clear_screen(cs)
        return -1



def print_session_menu(client_socket):
    client_socket.send("--------MENU----------\n".encode())
    client_socket.send("1. Create a new note\n".encode())
    client_socket.send("2. View all notes\n".encode())
    client_socket.send("3. Delete a note\n".encode())
    client_socket.send("4. Exit\n\n".encode())

def handle_session_input(inp, uid, cs):
    if inp == "1":
        #return("Create a new note")
        notes.create_note(uid, cs)
        time.sleep(2)
        return 1
    elif inp == "2":
        user_notes = notes.get_notes(uid)
        for n in user_notes:
            print(n)
            cs.send(f"{n}\n".encode())
        cs.send("Press enter to continue...".encode())
        cs.recv(1024)
        # return 2
    elif inp == "3":
        return("Delete a note")
        # return 3
    elif inp == "4":
        # return("Exit")
        return 4
    else:
        return("Invalid input")
        # return 5

def register(cs):
    attempts = 0
    clear_screen(cs)
    while attempts <= 3:
        if attempts == 3:
            cs.send("Too many attempts. Exiting...".encode())
            time.sleep(2)
            cs.close() # See if this works or if it needs to be in the main function

        cs.send("Enter a username: ".encode())
        username = cs.recv(1024).strip().decode()
        cs.send("Enter a password: ".encode())
        password = cs.recv(1024).strip().decode()

        ue = sql_funcs.check_if_user_exists(username, Debug=True)
        
        if not ue:
            sql_funcs.insert_user(username, password)
            cs.send("User created! Please login.\n".encode())
            time.sleep(2)
            clear_screen(cs)
            return
        else:
            cs.send("That username is taken! Please try again.\n".encode())
            time.sleep(2)
            clear_screen(cs)

def login(client_socket):
    username_prompt = "Enter your username: "
    password_prompt = "Enter your password: "
    success = False
    attempts = 0
    user = -1
    while not success:
        if attempts < 3:
            client_socket.send(username_prompt.encode())
            username = client_socket.recv(1024).strip().decode()
            password = ""
            ### DEPRECATED - REMOVE THIS BECAUSE REGISTRATION EXISTS
            if username == "creatister": # CREATE A NEW USER BUT THIS IS NOT ADVERTISED TO USERS. ONLY FOR TESTING
                # combination of create and register
                client_socket.send("\nEnter a username for the new user: ".encode())
                username = client_socket.recv(1024).strip().decode()
                client_socket.send("\nEnter a password for the new user: ".encode())
                password = client_socket.recv(1024).strip().decode()
                sql_funcs.insert_user(username, password)
                client_socket.send("User created!".encode())
                time.sleep(2)
                clear_screen(client_socket)
            else:
                client_socket.send(password_prompt.encode())
                password = client_socket.recv(1024).strip().decode()

            print(f"Received credentials - Username: {username}, Password: {password}")
            print(f"Checking login...")

            (password_correct, user) = sql_funcs.authenticate_user(username, password)
            if not password_correct:
                client_socket.send("Username or Password is incorrect. Please try again.".encode())
                time.sleep(2)
                clear_screen(client_socket)
                attempts += 1
            else:
                print(f"Password is correct. Logging in...")
                success = True
        else:
            client_socket.send("Too many failed login attempts. Please try again later.".encode())
            time.sleep(2)
            clear_screen(client_socket)
            client_socket.close()
            return -1
    client_socket.send(f"Welcome back {username}!".encode())
    time.sleep(2)
    clear_screen(client_socket)
    return user