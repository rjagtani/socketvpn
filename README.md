## SocketVPN

### 1. Introduction

This is a socket-based message passing VPN which takes a message from the client, encrypts it and sends it to the server.
The server decrypts the message and forwards it to the App Server. The App Server sends back the same message after 
appending some text. The server then encrypts this message and sends it back to the client, which decrypts it and
prints it. The aim of this repo is to mimic the basic functionalities of a VPN using socket programming

### 2. Diagram

[Insert diagram]

### 3. Working

1. Client establishes connection with server and the server asks for authentication.
2. Once authentication is done, the client is asked to input a message
3. This message is then encrypted on the client side using an encryption framework (which is selected in config)
4. The encrypted message is sent from client socket and received on server socket which decrypts it using the decryption key
5. The decrypted message is then forwarded to the App Server which receives it, appends some text and sends it back
6. The entire cycle then proceeds in reverse as the server encrypts the response and the client decrypts it

### 4. Steps to run the code
1. Clone the repo.
2. :warning: Install python > 3.8. This repo has been tested on python 3.10
3. Install requirements using this command: `pip install -r requirements.txt`.
4. Change server and app server address in config if running on separate machines, no changes needed if running locally
5. Run AppServer.py, TunnelServer.py and TunnelClient.py in this order
6. Enter password 'hithere' for successful authorization. It is matched against password hash which is stored in config
7. You will then be prompted to enter messages which will then follow the process explained in section 3
8. Enter message 'q' to exit the while loop and close the socket.

 
