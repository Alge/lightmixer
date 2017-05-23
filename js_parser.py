import js2py
from multiprocessing import Process, Queue
from instruction import Instruction
from script import Script
from helpers import current_milli_time

class JS_Parser:

    def parse_script(self, queue, code):

        js = """
        var now = 0

        var script = {
            name: "",
            instructions: [],
            repetitions: 1,
            start_time: 0,
        };

        function start_time(t){
            script.start_time = t;
        }

        function repeat(n){
            script.repetitions = n;
        }

        function wait(t){
            now = now + t;
        }

        function name(name){
            script.name = name;
        }

        function instruction(universe, channel, value, starttime, duration){
            script.instructions.push({"u":universe, "c":channel, "v":value, "start":starttime, "duration": duration});
        }

        //start of user code
        """ + code + """
        //end of user code

        //Return the script variable as a json string
        script
        """

        result = js2py.eval_js(js)

        s = Script(name=result["name"], repetitions=result["repetitions"])

        start = result["start_time"]
        if start == 0:
            start = current_milli_time()

        for i in result["instructions"]:

            instruction = Instruction(
                    universe=i["u"],
                    channel=i["c"],
                    color=i["v"],
                    start_time=start+i["start"],
                    stop_time=start + i["start"]+ i["duration"]
            )

            s.addInstruction(instruction)

        queue.put(s)
        #return s

    def execute(self, js, timeout = 5):
        q = Queue()
        p = Process(target=self.parse_script, args=(q, js))
        p.start()
        result = None
        try:
            result = q.get(block=True, timeout=timeout)
        except:
            try: #Race condition. if the process already terminated the terminate() method will throw a error.
                p.terminate()
            except:
                pass
            print("the script parser took too long time, killing the subprocess")

        return result



if __name__ == '__main__':
    p = JS_Parser()

    js = """
    name("hej")
    repeat(400)
    for(n = 0; n<5; n++){
        instruction(0,n,100, now, 1000)
    }
    wait(1000)
    for(n = 0; n<5; n++){
        instruction(0,2,0, now, 1000)
    }
    """

    print(p.execute(js, 4))







