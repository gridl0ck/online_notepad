import sqlite3
from sqlite3 import Error
import hashlib

#Change this to the location of the database
DATABASE_LOCATION = "/home/gridl0ck/proj/online_notepad/note_app.db"
#DATABASE_LOCATION = "C:\Users\Public\Documents\online_notepad\note_app.db"

def check_database():
    database_name = DATABASE_LOCATION

    conn = create_connection(database_name)

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone()

    if not table_exists:
        create_users_table(conn)
        create_notes_table(conn)
        print("Database and tables have been created.")
        conn.close()
    conn.close()

def check_if_user_exists(username, Debug=False):
    conn = create_connection(DATABASE_LOCATION)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username=?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    if Debug:
        print(f"Looking for user: {username}...")
        print(f"Results of query: {cursor.fetchall()}")
    if user is None:
        conn.close()
        return False
    else:
        conn.close()
        return True
    

def check_if_password_correct(username, password):
    conn = create_connection(DATABASE_LOCATION)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    if user is None:
        conn.close()
        return False
    else:
        conn.close()
        return True

def check_login(username, password):
    """Check if user exists and if password is correct"""
    conn = create_connection(DATABASE_LOCATION)
    user_exists = check_if_user_exists(username)
    if not user_exists:
        conn.close()
        return False
    else:
        password_correct = check_if_password_correct(username, password)
        conn.close()
        if not password_correct:
            return False
        else:
            return True

def create_connection(database_name):
    """Creates a connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(database_name)
        print(f'Successful connection to {database_name}...')
    except Error as e:
        print(e)

    return conn

def check_if_db_exists(database_name):
    """Check if database exists"""

    try: 
        conn = create_connection(database_name)
        conn.close()
        return True
    except Error as e:
        return False

def create_users_table(conn):
    """Create a table named 'users' with 'id' and 'username' columns"""
    try:
        cursor = conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    next_note_id INTEGER,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                );"""
        cursor.execute(query)
        print("The 'users' table has been created...")
    except Error as e:
        print(e)

def create_notes_table(conn):
    # Create a table named 'notes' with 'id', 'user_id' and 'text' columns
    try:
        cursor = conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    note_id INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    note TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );"""
        cursor.execute(query)
        print("The 'notes' table has been created...")
    except Error as e:
        print(e)

# Define a function to hash the password
def hash_password(password):
    # Convert the password to bytes and hash it using SHA256
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashlib.sha256(password_bytes).digest()

    # Convert the hashed bytes back to a string and return it
    hashed_password = hashed_bytes.hex()
    return hashed_password


def username_exists(username):
    # Connect to the database and check if a row exists in the 'users' table with the given username
    conn = sqlite3.connect(DATABASE_LOCATION)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    result = c.fetchone()

    # Close the connection and return True if a row was found, otherwise return False
    conn.close()
    return result is not None

def insert_user(username, password):
    hashed_password = hash_password(password)

    if username_exists(username):
        return False

    conn = sqlite3.connect('/home/gridl0ck/proj/online_notepad/note_app.db')
    c = conn.cursor()

    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))

    conn.commit()
    conn.close()

def authenticate_user(username, password):
    # Hash the password
    hashed_password = hash_password(password)

    conn = sqlite3.connect(DATABASE_LOCATION)
    c = conn.cursor()
    c.execute('SELECT password, id FROM users WHERE username = ?', (username,))
    result = c.fetchone()

    # If no result was found for the given username, return False
    if not result:
        return (False, -1)

    # If a result was found, retrieve the hashed password and compare it to the entered password
    stored_password = result[0]
    user_id = result[1]
    authenticated = hashed_password == stored_password

    # Close the connection and return the authentication result
    conn.close()
    return (authenticated, user_id)

if __name__ == "__main__":
    print("This is not mean to be run standalone")