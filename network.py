import socket
import re
import threading
from js_parser import JS_Parser

class tcp_instruction(threading.Thread):

    def __init__(self, instruction_port = 10000, instruction_IP = "127.0.0.1", message_queue = None):
        threading.Thread.__init__(self)
        self.instruction_buffer_size = 100000
        self.instruction_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.instruction_socket.bind((instruction_IP, instruction_port))
        self.message_queue = message_queue

        #Compile the regex here so we won't need to do it every time
        self.r = re.compile(r"(?P<universe>[0-9]+):(?P<channel>[0-9]+):(?P<value>[0-9]+);?")

    def extract_data(self, message):

        data = self.r.findall(message)
        return [(int(s[0]), int(s[1]), int(s[2])) for s in data]


    def run(self):

        self.instruction_socket.listen(100)
        print("started listening on instruction socket")

        while 1:

            try:
                conn, addr = self.instruction_socket.accept()
                print("Connection from: {}".format(addr))
                while 1:
                    data = conn.recv(self.instruction_buffer_size)
                    if not data: break #no data :/

                    for i in self.extract_data(str(data)):
                        self.message_queue.put(i)
                    print("recieved set of instructions: {}. size of queue is approx. {}".format(self.extract_data(str(data)), self.message_queue.qsize()))
                conn.close()
            except Exception as e:
                print(e)

class tcp_script(threading.Thread):

    def __init__(self, instruction_port = 10001, instruction_IP = "127.0.0.1", script_queue = None):
        threading.Thread.__init__(self)
        self.instruction_buffer_size = 100000
        self.instruction_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.instruction_socket.bind((instruction_IP, instruction_port))
        self.script_queue = script_queue
        self.port = instruction_port
        self.ip = instruction_IP


    def run(self):

        self.instruction_socket.listen(100)
        print("started listening on script socket on port: {}".format(self.port))

        while 1:
            try:
                conn, addr = self.instruction_socket.accept()
                print("Connection with script from: {}".format(addr))

                js = ""
                while 1:
                    data = conn.recv(self.instruction_buffer_size)

                    if not data: break #no more data :/
                    js = js + data.decode("utf-8")

                conn.close()
                print("recieved data on the script socket: {}".format(js))
                jsp = JS_Parser()
                script = jsp.execute(js)
                self.script_queue.put(script)

            except Exception as e:
                print(e)

if __name__ == '__main__':
    s = tcp_script()
    s.run()