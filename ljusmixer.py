from time import time, sleep

from client import Client

current_milli_time = lambda: int(round(time() * 1000))

class Mixer:

    universes = []
    num_universes = 0;
    universe_size = 0

    clients = []

    script_list = []

    last_run_time = 0
    current_time = 0
    time_delta = 0


    def __init__(self, universes, universe_size = 513, fps = 60):
        self.num_universes = universes
        self.universe_size = universe_size

        self.universes = self.create_universes()

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


    def run_scripts(self):

        for script in self.script_list:
                script.tick(current_time=self.current_time)


    def copy_scripts(self):

        self.universes = self.create_universes()

        for script in self.script_list:
            for (universe, channel) in script.active_values:
                value = script.universes[universe][channel]
                #print("Found value {}, adding it to universe: {}, channel {}".format(value, universe, channel))
                self.universes[universe][channel] += round(script.universes[universe][channel])
                if self.universes[universe][channel] > 255:
                    self.universes[universe][channel] = 255

    def update_clients(self):
        for client in self.clients:
            client.send_data(self.universes[client.universe])


    def run(self):
        while 1:
            self.last_run_time = self.current_time
            self.current_time = current_milli_time()
            self.time_delta = self.current_time-self.last_run_time
            print("Frames per second: {}".format(1/(self.time_delta/1000.0)))
            #print(self.universes[0][:5])

            self.run_scripts()
            self.copy_scripts()
            self.update_clients()

            #Sleep the rest of the time (16 -> ~60fps, 25 -> ~40fps)
            sleep(abs((16-(current_milli_time()-self.current_time))/1000))