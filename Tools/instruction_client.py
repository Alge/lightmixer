import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

conn = s.connect(("127.0.0.1", 9000))

message = "Hello!".encode()

s.send(message)
#s.close()

