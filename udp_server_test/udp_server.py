import socket

HOST = '0.0.0.0'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))

    print("UDP Server is listening on port", PORT, flush=True)

    while True:
        data, addr = server_socket.recvfrom(1024)

        print("Received from client:", data.decode(), flush=True)

        server_socket.sendto(data, addr)
