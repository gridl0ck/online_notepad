# online_notepad

## Purpose
This application was developed for myself to use as a sort of replacement for the Microsoft Sticky Notes application. As I was using a Linux machine and often did not want to go through the hassle of trying to access the web version (and having to go through the Microsoft Sign-in nonsense) every time I wanted to create a note, I simply ran this on my home network and could simply netcat to the server, login to the service, and write myself notes.

## Features
*__THIS IS A WORK IN PROGRESS APPLICATION AND IS INCOMPLETE__*
As of now, the only functionality that I need for this application is the ability to:
  - Create an account
  - Login to an account
  - Create a note
  - Delete a note
  - List all of your notes
    
I am not sure I will add anything else to this, but there is a potential idea to create a client to allow decentralized storage of your notes, then uploading and ensuring the database matches the server one.

## Usage
Simply run the `server.py` file in a your directory of your choosing to initialize the database. Then, as of now simply use netcat to connect to the port specified at launch on either localhost or a machine on your network. There are menu's that allow you to describe what to do.

## Future Work
- Figure out multi-user database interfacing
- Client to allow for offline note creation then uploading to central server (redundancy)
- ~~Create `requirements.txt` to streamline script initialization~~ Uses all standard library modules
- ~~Installation script???~~ Nothing to install... yet...
