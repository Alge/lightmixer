from ljusmixer import Mixer
from instruction import Instruction
from script import Script
from time import time


if __name__ == '__main__':


    m = Mixer(universes=10, universe_size=513, fps=4)

    instructions = []

    #def __init__(self, universe, channel, start, finish, startTime = 0, stopTime = 0):

    current_milli_time = lambda: int(round(time() * 1000))


    now = current_milli_time()

    for _ in range(3):
        script = Script(2)

        for u in range(5):
            for i in range(500):
                script.addInstruction(Instruction(universe=u, channel=i, color=1*i, start_time=now, stop_time=now + 5000))

    m.add_client(address="127.0.0.1", port=10000, universe=0)

    m.add_script(script)
    m.run()