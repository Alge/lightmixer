import datetime
class Instruction:

    def __init__(self, universe, channel, color, start_time = 0, stop_time = 0):
        self.universe = universe
        self.channel = channel
        self.start_time = start_time
        self.stop_time = stop_time
        self.color = color
        self.change_vector = None
        self.started = False
        self.done = False
        self.value = 0

    def __str__(self):
     return "Instruction. Universe: {}, channel: {}, change vector: {}, color: {}, value: {}, started: {}, done: {}, start time: {}, stop time: {}".format(
             self.universe,
             self.channel,
             self.change_vector,
             self.color,
             self.value,
             self.started,
             self.done,
             self.start_time,
             self.stop_time
     )

