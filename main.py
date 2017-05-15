from ljusmixer import Mixer
from instruction import Instruction
from script import Script
from time import time


if __name__ == '__main__':


    m = Mixer(10, 513)

    instructions = []

    #def __init__(self, universe, channel, start, finish, startTime = 0, stopTime = 0):

    current_milli_time = lambda: int(round(time() * 1000))


    now = current_milli_time()

    script = Script(100)

    for i in range(500):
        script.addInstruction(Instruction(universe=0, channel=i, color=1*i, start_time=now, stop_time=now + 300000))
    for i in range(500):
        script.addInstruction(Instruction(universe=0, channel=i, color=0, start_time=now + 5000, stop_time=now + 10000))

    m.add_script(script)

    for _ in range(1):
        script = Script(100)

        for u in range(4):
            for i in range(500):
                script.addInstruction(Instruction(universe=u, channel=i, color=20*i, start_time=now, stop_time=now + 300000))
            for i in range(500):
                script.addInstruction(Instruction(universe=u, channel=i, color=0, start_time=now + 300000, stop_time=now + 300000+1000))

    m.add_client(address="192.168.1.199", port=10000, universe=0)

    m.add_script(script)
    m.run()