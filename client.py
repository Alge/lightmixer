import socket, struct

class Client:

    address = None
    port = None
    universe = None

    def __init__(self, address, port, universe):
        self.address = address
        self.port = port
        self.universe = universe
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data):
        #print("Sending data: {}".format(data))
        self.socket.sendto(self.encode_array(data), (self.address, self.port))

    def encode_array(self, in_array):
        out = []
        for i in in_array:
            out.append(i.to_bytes(1, byteorder='big'))
        outbuffer = struct.pack("!{}c".format(len(out)), *out)

        return outbuffer