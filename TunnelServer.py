import socket
from Crypto.Cipher import AES
import config
import hashlib

# AES encryption key
key = config.ENCRYPTION_KEY

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = config.SERVER_ADDRESS
print(f'starting up on {server_address}')
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
sock_app_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
app_server_address = config.APP_SERVER_ADDRESS
print(f'connecting to {app_server_address}')
sock_app_server.connect(app_server_address)

incorrect_password_attempts = 0
while True:
    # Wait for a connection
    print('waiting for a connection')

    connection, client_address = sock.accept()

    try:
        # Authentication of client password
        print(f'connection from {client_address}')
        password_to_check = connection.recv(16)
        hashed_pwd = config.PASSWORD['client1']
        salt_from_password = hashed_pwd[:32]  # 32 is the length of the salt
        key_from_password = hashed_pwd[32:]
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            password_to_check,  # Convert the password to bytes
            salt_from_password,
            100000
        )
        if new_key == key_from_password:
            auth_message = "auth success"
            connection.sendall(auth_message.encode('utf-8'))
            while True:
                # Receive encrypted data from the client and decrypt it
                data = connection.recv(16)
                print(f'Server: received encrypted text from client: {data}')
                if data:
                    nonce_tag = connection.recv(16+16)
                    nonce,tag = nonce_tag[:16], nonce_tag[16:]
                    cipher = AES.new(key, AES.MODE_EAX, nonce)
                    plaintext = cipher.decrypt(data)
                    print(f'Server: forwarding decrypted data to app server: {plaintext}')
                    # Sending data to AppServer from here
                    sock_app_server.sendall(plaintext)
                    app_data = sock_app_server.recv(65444)
                    app_data_decode = app_data.decode('utf-8')
                    print(f'Server: Received response from App server: {plaintext}')
                    app_data_send = app_data_decode

                    # Receive response from AppServer, encrypt it and send it to client
                    cipher1 = AES.new(key, AES.MODE_EAX)
                    nonce1 = cipher1.nonce
                    ciphertext, tag1 = cipher1.encrypt_and_digest(app_data_send.encode('utf-8'))
                    print(f'Server: Sending encrypted response to Client: {ciphertext}')
                    connection.sendall(ciphertext)
                    nn1 = nonce1 + tag1
                    connection.sendall(nn1)

                else:
                    print('no more data from', client_address)
                    break
        else:

            incorrect_password_attempts += 1
            auth_message = "Inc pwd" + str(incorrect_password_attempts)
            connection.sendall(auth_message.encode('utf-8'))
            print("Incorrect Password Attempt: " + str(3-incorrect_password_attempts) + " attempts left")
            # Stop listening to requests if 3 incorrect attempts are made
            if incorrect_password_attempts == 3:
                break
    finally:
        # Clean up the connection
        connection.close()