import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
app_server_address = ('localhost', 40000)
print(f'starting up on {app_server_address}')
sock.bind(app_server_address)

sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, server_address = sock.accept()
    try:
        print(f'connection from {server_address}')
        while True:
            data = connection.recv(16)
            if data:
                data_decode = data.decode('utf-8')
                data_send = 'Reached App Server: ' + data_decode
                data_send = data_send.encode('utf-8')
                connection.sendall(data_send)
            else:
                print('no more data from', server_address)
                break
    finally:
        # Clean up the connection
        connection.close()