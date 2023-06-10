from sql_stuff.sql_funcs import create_connection
from sql_stuff.sql_funcs import DATABASE_LOCATION
import sys

### TODO
# write a function to go back through all user notes and update the ID
# if a note was deleted and the number is less than the number of total notes


# This function should be able to edit the id of the note 
def edit_note_id(cs, uid, op, note_id):
    """Edit the next_note_id for a user"""
    if note_id == 0 and op != "add": # redundant check
        cs.send("No notes to delete\n".encode())
        return
    vall = 1 if op == "add" else -1
    conn = create_connection(DATABASE_LOCATION)
    cursor = conn.cursor()
    updated_id = int(note_id) + vall
    print(f"SETTING next_note_id TO {updated_id}")
    query = """UPDATE users SET next_note_id=? WHERE id=?;"""
    cursor.execute(query, (uid, updated_id,))
    conn.commit()
    conn.close()



# This is a temporary test of functionality that the above function should be doign
# OPCODES: 
# 3 = add
# 4 = subtract
def update_user_note_count(cs, uid, op):

    q = """SELECT next_note_id FROM users WHERE id=?;"""
    conn = create_connection(DATABASE_LOCATION)
    cursor = conn.cursor()

    cursor.execute(q, (uid,))
    note_id = cursor.fetchone()[0]
    conn.close()
    print(note_id)
    # sys.exit(0)
    updated_value = int(note_id) + 1
    q2 = """UPDATE users SET next_note_id=? WHERE id=?;"""
    conn = create_connection(DATABASE_LOCATION)
    cursor = conn.cursor()
    cursor.execute(q2, (str(updated_value),uid,))
    cursor.execute(q, (uid,))
    new_id = cursor.fetchone()[0]
    print(new_id)
    conn.close()
    # sys.exit(0)

def create_note(u, cs):
    """Create a note for a user"""
    uid = u
    conn = create_connection(DATABASE_LOCATION)

    cs.send("Enter your note: ".encode())
    message = cs.recv(1024).decode()
    cursor = conn.cursor()
    q = """SELECT next_note_id FROM users where id=?;"""
    cursor.execute(q, (uid,))
    curr_note_id = cursor.fetchone()[0]
    query = """INSERT INTO notes (user_id, note, note_id) VALUES (?, ?, ?);"""
    print(f"Note ID to be added: {curr_note_id}")
    cursor.execute(query, (uid, message, curr_note_id))
    conn.commit()
    conn.close()
    print(f"Current ID of the current note {curr_note_id}")
    edit_note_id(cs, uid, "add", curr_note_id)
    update_user_note_count(cs, uid, 3)
    cs.send("Note created successfully!".encode())
    

def get_notes(id):
    """Get all notes for a user"""
    conn = create_connection(DATABASE_LOCATION)
    cursor = conn.cursor()
    query = """SELECT * FROM notes WHERE user_id=?;"""
    cursor.execute(query, (id,))
    notes = cursor.fetchall()
    conn.close()
    return notes

def print_notes(notes, cs):
    """Print all notes for a user"""
    # cs.send("Here are your notes:\n".encode())
    for note in notes:
        cs.send(f"{note[0]}: {note[2]}\n".encode())

def delete_note(cs, uid):
    """Delete a note for a user"""
    conn = create_connection(DATABASE_LOCATION)
    cursor = conn.cursor()
    notes = get_notes(uid)
    if len(notes) == 0:
        cs.send("User has no notes.\n".encode())
        return
    cs.send("Enter the ID of the note you want to delete: ".encode())
    query = """DELETE FROM notes WHERE note_id=? AND user_id=?;"""
    cursor.execute(query, (nid,uid))
    conn.commit()
    conn.close()