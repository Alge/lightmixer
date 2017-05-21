from ljusmixer import Mixer
from instruction import Instruction
from script import Script
from time import time

current_milli_time = lambda: int(round(time() * 1000))

if __name__ == '__main__':

    m = Mixer(universes=10, universe_size=20, fps=40)

    now = current_milli_time()

    for _ in range(1):

        script = Script( repetitions=100)
        u = 0
        for k in range(5):
            script.addInstruction(Instruction(universe=u, channel=k, color=5*(k+1), start_time=now, stop_time=now + 3000))
        for l in range(5):
            script.addInstruction(Instruction(universe=u, channel=l, color=0, start_time=now + 3000, stop_time=now + 3000+2000))
        print("Adding instruction to script: {}".format(script))
        m.add_script(script)

    m.add_client(address="127.0.0.1", port=10000, universe=0)


    m.run()