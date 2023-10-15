import socket
import threading
import sqlite3
import custom_functions.sql_funcs as sql_funcs
import custom_functions.server_func as server_func
import custom_functions.note as note
import os
import time

#TODO
# Create server-wide windows netcat checks for compatibility
# Leave comments on server functions, note functions, and sql helper functions
# Remove extra functions/move to correct classes
# Standardize response codes

def init_database_location(directory=None):
    """Takes in a directory and creates a database in that location"""
    if directory is None:

        directory = os.path.expanduser("~")
        # print(filename)
    else:
        if not os.path.exists(directory):
            os.makedirs(directory)

    filename = os.path.join(directory, "notes-database.db")
    os.environ['DATABASE_LOCATION'] = filename

    sql_funcs.init_sql_vars()
    server_func.init_server_vars()
    note.init_note_vars()

def handle_client(client_socket):
    server_func.clear_screen(client_socket)
    client_socket.send("Welcome to the Online Notepad!\n\n".encode())
    resp_code = -1
    user_id = -1
    while resp_code == -1:
        resp_code = server_func.print_main_menu(client_socket)
        user_id = resp_code

    if resp_code == -2:
        return
    cont = True
    while cont:
        server_func.print_session_menu(client_socket)
        client_socket.send("Please enter your choice: ".encode())
        choice = client_socket.recv(1024).strip().decode()
        opcode = server_func.handle_session_input(choice, user_id, client_socket)
        if opcode == 4:
            client_socket.send("Goodbye!".encode())
            time.sleep(2)
            client_socket.close()
            return
        server_func.clear_screen(client_socket)
    client_socket.close()

def main():

    init_database_location()

    sql_funcs.check_database()
    host = "0.0.0.0"  # Bind to all available network interfaces
    port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))

    server.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client, addr = server.accept()
        print(f"[*] Connection accepted from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    main()