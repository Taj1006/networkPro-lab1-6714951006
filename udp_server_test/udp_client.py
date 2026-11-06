import socket

HOST = 'udp_server'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    print("UDP Client is ready.")

    while True:
        message = input("Enter message (type 'exit' to quit): ")

        if message.lower() == 'exit':
            break

        client_socket.sendto(message.encode(), (HOST, PORT))

        data, addr = client_socket.recvfrom(1024)

        print("Received from server:", data.decode())
