import socket, struct

UDP_IP = "127.0.0.1"
UDP_PORT = 10000

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print ("received message:", [int.from_bytes(data[i:i+1], byteorder='big') for i in range(0, len(data))])