from time import time, sleep
import threading
from client import Client

current_milli_time = lambda: int(round(time() * 1000))

class Mixer(threading.Thread):
    def __init__(self, universes, universe_size = 513, fps = 60, instruction_queue = None, script_queue = None):

        threading.Thread.__init__(self)

        self.instruction_queue = instruction_queue
        self.script_queue = script_queue

        self.clients = []

        self.script_list = []

        self.last_run_time = 0
        self.current_time = 0
        self.time_delta = 0

        self.num_universes = universes
        self.universe_size = universe_size
        self.fps = fps

        self.universes = self.create_universes()
        self.tcp_universes = self.create_universes()
        self.used_channels_tcp = set()

        self.done_scripts = []

    def create_universes(self):
        u = []
        for i in range(self.num_universes):
            u.append([0] * self.universe_size)
        return u

    def add_script(self, script):
        self.script_list.append(script)


    def add_client(self, address, port, universe):
        if universe > self.num_universes:
            return False
        self.clients.append(Client(address = address, port = port, universe = universe))
        return True

    def remove_client(self, address, port, universe):
        for c in self.clients:
            if c.address == address and c.port == port and c.universe == universe:
                self.clients.remove(c)

    def get_new_scripts(self):
        while not self.script_queue.empty():
            print("Added a script from the queue")
            self.add_script(self.script_queue.get())

    def run_scripts(self):

        for script in self.script_list:
                script.tick(current_time=self.current_time)
                if script.done:
                    print("Script: {} done".format(script))
                    self.done_scripts.append(script)

    def handle_done_scripts(self):
        while len(self.done_scripts)>0:
            s = self.done_scripts.pop()
            if s.repetitions > 1:
                s.reset()
                s.repetitions -=1
            else:
                self.script_list.remove(s)

    def copy_scripts(self):

        self.universes = self.create_universes()

        for script in self.script_list:
            #print(script.universes)
            for (universe, channel) in script.active_values:
                value = script.universes[universe][channel]
                #print("Found value {}, adding it to universe: {}, channel {}".format(value, universe, channel))
                self.universes[universe][channel] += round(script.universes[universe][channel])
                if self.universes[universe][channel] > 255:
                    self.universes[universe][channel] = 255

    def update_clients(self):
        for client in self.clients:
            client.send_data(self.universes[client.universe])


    def get_tcp_instructions(self):
        while not self.instruction_queue.empty():
            instruction = self.instruction_queue.get()
            universe = instruction[0]
            channel = instruction[1]
            value = instruction[2]
            if self.num_universes <= universe or self.universe_size <= channel:
                print("Instruction for universe {} and channel {} (value {}) failed as it does not conform to the universe/channel sizes".format(universe,channel,value))

            elif value == 0: #Just remove the channel from the set of used channels so it will be ignored in calculations
                self.used_channels_tcp.discard((universe, channel))
                self.tcp_universes[universe][channel] = 0 #Shouldn't be necessary as the channel isn't in the update list, but might be good for the future
            else :
                self.used_channels_tcp.add((universe, channel))
                if value> 255:
                    value = 255
                self.tcp_universes[universe][channel] = value

            print("recieved a instruction for universe: {}, channel: {}. New value: {}".format(instruction[0],instruction[1],instruction[2]))


    def copy_tcp_instructions(self):
        for location in self.used_channels_tcp:
            self.universes[location[0]][location[1]] += round(self.tcp_universes[location[0]][location[1]])
            if self.universes[location[0]][location[1]] > 255:
                self.universes[location[0]][location[1]] = 255
            #print("copied tcp instruction:{}:{}:{}".format(location[0], location[1], self.tcp_universes[location[0]][location[1]]))

    def run(self):
        while 1:
            self.last_run_time = self.current_time
            self.current_time = current_milli_time()
            self.time_delta = self.current_time-self.last_run_time
            #print("{} FPS".format(round(1/(self.time_delta/1000.0))))

            self.get_new_scripts()
            self.run_scripts()
            self.get_tcp_instructions()
            self.copy_scripts()
            self.copy_tcp_instructions()
            self.update_clients()
            self.handle_done_scripts()

            #Sleep the rest of the time (16 -> ~60fps, 25 -> ~40fps)
            sleeptime = ((1000/self.fps)-(current_milli_time()-self.current_time))/1000
            if sleeptime > 0:
                sleep(sleeptime)

