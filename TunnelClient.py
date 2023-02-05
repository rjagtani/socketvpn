import socket
from Crypto.Cipher import AES
import config

# AES encryption key (should be the same as the one used on the server)
key = config.ENCRYPTION_KEY

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = config.SERVER_ADDRESS
print(f'connecting to {server_address}')
sock.connect(server_address)

try:
    # Enter password
    client_password = input("Enter Password:")
    sock.sendall(client_password.encode('utf-8'))

    # Receive auth message
    auth_message = sock.recv(65444)
    auth_message = auth_message.decode('utf-8')
    print(auth_message)
    if auth_message == "auth success":
        message_str = input("-> ")
        while message_str != 'q':
            # Encode message to bytes
            message = str.encode(message_str)
            print(f'sending {message}')

            # Send message to server after encryption
            cipher = AES.new(key, AES.MODE_EAX)
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(message)
            sock.sendall(ciphertext)
            sock.sendall(nonce + tag)

            # get encrypted response from server and decrypt it
            data = sock.recv(65455)
            #print(data)
            nonce_tag1 = sock.recv(16 + 16)
            nonce1, tag1 = nonce_tag1[:16], nonce_tag1[16:]
            cipher1 = AES.new(key, AES.MODE_EAX, nonce1)
            plaintext = cipher1.decrypt(data)
            plaintext = plaintext.decode('utf-8')

            print(f'received {plaintext}')
            message_str = input("-> ")
        sock.close()
        print('closing socket')
    else:
        # Closes socket when incorrect password is entered
        print("Incorrect Password")
        sock.close()
        print('closing socket')
finally:
    pass
    # Clean up the connection


