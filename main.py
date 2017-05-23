from ljusmixer import Mixer
from instruction import Instruction
from network import tcp_instruction, tcp_script
from script import Script
from time import time, sleep
import queue
import threading

current_milli_time = lambda: int(round(time() * 1000))

if __name__ == '__main__':

    #Set up the network threads

    #Tcp instructions
    instruction_queue = queue.Queue()

    net_instruction = tcp_instruction(instruction_port=9000, instruction_IP="127.0.0.1", message_queue=instruction_queue)
    net_instruction.daemon = True #No point in keeping the thread alive when main program has exited
    net_instruction.start()

    #Tcp scripts
    script_queue = queue.Queue()

    net_script = tcp_script(instruction_port=9001, instruction_IP="127.0.0.1", script_queue=script_queue)
    net_script.daemon = True
    net_script.start()


    #Set up the mixer
    m = Mixer(universes=1, universe_size=20, fps=600, instruction_queue=instruction_queue, script_queue=script_queue)
    m.daemon = True
    now = current_milli_time()

    """
    for _ in range(1):

        script = Script(name="Testscript", repetitions=2)
        u = 0
        for k in range(1):
            script.addInstruction(Instruction(universe=u, channel=k, color=255, start_time=now, stop_time=now + 3000))
        for l in range(1):
            script.addInstruction(Instruction(universe=u, channel=l, color=0, start_time=now + 4000, stop_time=now + 4000+3000))
        print("Adding instruction to script: {}".format(script))
        m.add_script(script)
     """
    m.add_client(address="127.0.0.1", port=10000, universe=0)

    m.start() #start the mixer thread

    m.join() #the mixer thread should never return, this is just to keep the script running