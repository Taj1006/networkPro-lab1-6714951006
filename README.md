# Network Programming Lab 1
## TCP & UDP Echo Server using Python and Docker

### Student Information
- **Name:** ธัชพล ขจรชีพ
- **Student ID:** 6714951006
- **Operating System:** Ubuntu Linux
- **Programming Language:** Python
- **Container Platform:** Docker

---

## 1. Objective

This laboratory demonstrates network communication
between a Python client and server using TCP and UDP
protocols within Docker containers.

## 2. TCP Echo Server

TCP provides reliable, connection-oriented communication.

### Docker Commands

```bash
cd tcp_echo_server

docker network create echo_network

docker build -f Dockerfile.server -t echo_server .
docker build -f Dockerfile.client -t echo_client .

docker run -d --name echo_server --network echo_network echo_server
docker run -it --name echo_client --network echo_network echo_client
```

### TCP Test Result

The TCP client successfully sent three messages to the
server and received identical messages in response.

![TCP Echo Server](screenshots/tcp.png)

---

## 3. UDP Echo Server

UDP provides connectionless, datagram-based communication.

### Docker Commands

```bash
cd udp_server_test

docker network create udp_network

docker build -f Dockerfile.server -t udp_server .
docker build -f Dockerfile.client -t udp_client .

docker run -d --name udp_server --network udp_network udp_server
docker run -it --name udp_client --network udp_network udp_client
```

### UDP Test Result

The UDP client successfully sent three messages to the
server and received identical messages in response.

![UDP Echo Server](screenshots/udp.png)

---

## 4. TCP vs UDP

| Feature | TCP | UDP |
|---|---|---|
| Connection | Connection-oriented | Connectionless |
| Reliability | Reliable | No delivery guarantee |
| Data Transfer | Byte stream | Datagrams |
| Python Socket | SOCK_STREAM | SOCK_DGRAM |
| Send Method | sendall() | sendto() |
| Receive Method | recv() | recvfrom() |

---

## 5. Conclusion

Both TCP and UDP Echo Servers were successfully
implemented using Python and Docker.

The experiments demonstrate communication between
containers connected to the same Docker network.

TCP provides reliable and ordered communication,
while UDP provides connectionless datagram transmission.
