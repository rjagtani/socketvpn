import socket
from Crypto.Cipher import AES
import config
from Crypto.Random import get_random_bytes
# AES encryption key
key = b'\x1c\xf3\xf5\x8ebp\x9a\x0f2|N\xb5\x06\x9d[\xa5'
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print(f'starting up on {server_address}')
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
sock_app_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the server's address and port
app_server_address = ('localhost', 20000)
print(f'connecting to {app_server_address}')
sock_app_server.connect(app_server_address)
#server_address = ('192.168.178.37', 10000)


while True:
    # Wait for a connection
    print('waiting for a connection')

    connection, client_address = sock.accept()
    incorrect_password_attempts = 0
    try:
        print(f'connection from {client_address}')
        password = connection.recv(16)
        if password.decode('utf-8') == config.PASSWORD['client1']:
            auth_message = "auth success"
            connection.sendall(auth_message.encode('utf-8'))
            while True:
                data = connection.recv(16)
                print(data)
                if data:
                    nonce_tag = connection.recv(16+16)
                    nonce,tag = nonce_tag[:16], nonce_tag[16:]
                    cipher = AES.new(key, AES.MODE_EAX, nonce)
                    plaintext = cipher.decrypt(data)

                    #Sending data to appserver from here
                    sock_app_server.sendall(plaintext)
                    app_data = sock_app_server.recv(65444)
                    app_data_decode = app_data.decode('utf-8')
                    app_data_send = 'Hello, this is your plaintext:' + app_data_decode

                    cipher1 = AES.new(key, AES.MODE_EAX)
                    nonce1 = cipher1.nonce
                    ciphertext, tag1 = cipher1.encrypt_and_digest(app_data_send.encode('utf-8'))
                    connection.sendall(ciphertext)
                    connection.sendall(nonce1 + tag1)

                else:
                    print('no more data from', client_address)
                    break
        else:
            incorrect_password_attempts += 1
            auth_message = "Inc pwd" + str(incorrect_password_attempts)
            connection.sendall(auth_message.encode('utf-8'))
            print("Incorrect Password Attempt: " + str(3-incorrect_password_attempts) + " attempts left")
            if incorrect_password_attempts == 3:
                break
    finally:
        # Clean up the connection
        connection.close()