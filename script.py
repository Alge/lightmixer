
class Script:

    universes = []
    sizes = []

    repetitions = 0

    instructions = []

    active_values = set()

    done = False

    def __init__(self, repetitions):
        self.repetitions = repetitions

    def addInstruction(self, instruction):

        #print("Trying to add instruction: {}".format(instruction))

        while len(self.universes) <= instruction.universe:
            self.universes.append([])
            self.sizes.append(0)

        #print(self.universes)
        while len(self.universes[instruction.universe]) <= instruction.channel:
            self.universes[instruction.universe].append(0)
            #print("Sizes: {}".format(self.sizes))
            self.sizes[instruction.universe] += 1
        self.instructions.append(instruction)

        self.active_values.add((instruction.universe, instruction.channel))

        #print("Added a new instruction: {}".format(instruction))
        #print(self.universes)

    def tick(self, current_time):
        self.runInstructions(current_time)
        self.copyInstructions()

    def runInstructions(self, current_time):
        self.done = True
        for i in self.instructions:
            if not i.done and i.stop_time<current_time:
                i.done = True
                i.value = i.color
                #print("instruction done: {}".format(i))
                continue

            elif not i.done and i.start_time<=current_time:
                self.done = False
                if not i.started:
                    i.started = True
                    i.color = i.color - self.universes[i.universe][i.channel]
                    i.change_vector = i.color/(i.stop_time - i.start_time)

                    #print("Started instruction: {}".format(i))

                i.value = i.change_vector*(current_time-i.start_time)
                #print(i)



    def copyInstructions(self):
        #print("Copying instructions")
        #print(self.sizes)
        #Empty the script buffer
        for i in range(len(self.sizes)):
            for ii in range(self.sizes[i]):
                #print("Universe: {} Channel: {}".format(i, ii))
                self.universes[i][ii] = 0

        #Fill it with new data
        for instruction in self.instructions:

            self.universes[instruction.universe][instruction.channel] += instruction.value

            if self.universes[instruction.universe][instruction.channel] < 0:
                self.universes[instruction.universe][instruction.channel] = 0
            elif self.universes[instruction.universe][instruction.channel] > 255:
              self.universes[instruction.universe][instruction.channel] = 255

        #print (self.universes)

    def __str__(self):
     return "Script. Number of instructions: {}".format(len(self.instructions))
