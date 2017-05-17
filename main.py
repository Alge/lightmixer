from ljusmixer import Mixer
from instruction import Instruction
from script import Script
from time import time

current_milli_time = lambda: int(round(time() * 1000))

if __name__ == '__main__':

    m = Mixer(universes=10, universe_size=513, fps=40)

    now = current_milli_time()

    for _ in range(4):
        script = Script(200)

        for u in range(5):
            for i in range(50):
                script.addInstruction(Instruction(universe=u, channel=i, color=1*i, start_time=now, stop_time=now + 5000))
            for i in range(500):
                script.addInstruction(Instruction(universe=u, channel=i, color=0, start_time=now + 6000, stop_time=now + 6000+5000))
        m.add_script(script)

    m.add_client(address="127.0.0.1", port=10000, universe=0)


    m.run()