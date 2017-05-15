import socket

class Network:

    instruction_buffer_size = 100000

    def __init__(self, instruction_port = 10000, instruction_IP = "127.0.0.1"):

        self.instruction_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.instruction_socket.bind(("127.0.0.1", 10000))

    def instruction_listener(self):

        self.instruction_socket.listen(100)
        print("started listening on instruction socket")

        while 1:
            conn, addr = self.instruction_socket.accept()
            print("Connection from: {}".format(addr))
            while 1:
                data = conn.recv(self.instruction_buffer_size)
                if not data: break #no data :/
                print("recieved data: {}".format(data))
                conn.send(data)
            conn.close()

n = Network()
n.instruction_listener()


"""
import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    conn.send(data)  # echo
conn.close()

"""