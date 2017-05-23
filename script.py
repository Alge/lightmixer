
class Script:

    def __init__(self, name = "", repetitions = 1):

        self.old_universes = None
        self.universes = []
        self.sizes = []
        self.name = name
        self.instructions = []
        self.active_values = set()
        self.done = False

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

        if self.old_universes == None: #This is the first time running the script, create a empty old universes list
            self.old_universes = []
            for i in self.sizes:
                self.old_universes.append([0]*i)

        self.done = True
        for i in self.instructions:

            if not i.done and i.stop_time<current_time: #If not done and should have stopped
                i.done = True
                i.value = i.to_value
                print("instruction done: {}".format(i))
                continue

            elif not i.done and i.start_time<=current_time:#If not done and should have started

                self.done = False
                if not i.started:
                    i.started = True
                    #print("new 'to_value: {}'. color: {}, universes value: {}. old_universes value:{}".format(i.color - (self.universes[i.universe][i.channel]+self.old_universes[i.universe][i.channel]), i.color, self.universes[i.universe][i.channel], self.old_universes[i.universe][i.channel]))
                    if self.universes[i.universe][i.channel] == 0: #The old universe value is copied into the new universe
                        i.to_value = i.color - (self.universes[i.universe][i.channel]+self.old_universes[i.universe][i.channel])
                    else:
                        i.to_value = i.color - (self.universes[i.universe][i.channel])
                    i.change_vector = i.to_value/(i.stop_time - i.start_time)

                    print("Started instruction: {}".format(i))
                    print("universes: {}, old_universes: {}".format(self.universes, self.old_universes))

                i.value = i.change_vector*(current_time-i.start_time)
                #print("running instruction {}".format(i))
            elif not i.done: #Needed to wait for later instructions
                #print("{} not ready to start yet".format(i))
                self.done = False
            #elif i.done:
            #    print("{} already done".format(i))

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
            #print("old value: {}, ".format(self.universes[instruction.universe][instruction.channel]))
            self.universes[instruction.universe][instruction.channel] += instruction.value
            #print("new value of channel: {} old universe: {} (instruction: {})".format(self.universes[instruction.universe][instruction.channel], self.old_universes, instruction))

            if self.universes[instruction.universe][instruction.channel] < 0:
                self.universes[instruction.universe][instruction.channel] = 0
            elif self.universes[instruction.universe][instruction.channel] > 255:
              self.universes[instruction.universe][instruction.channel] = 255

        #Add the old universe values.
        for location in self.active_values:
            self.universes[location[0]][location[1]] += self.old_universes[location[0]][location[1]]
        #print("self.universes after update: {}".format(self.universes))

        #print (self.universes)

    def reset(self): #Reset the script so it is ready to run again
        self.old_universes = self.universes[:]#Copy by value, not reference
        #print(self.old_universes is self.universes)

        self.universes = []
        for i in self.sizes:
            self.universes.append([0]*i)

        tstart = 99999999999999
        tstop = 0


        #Find the duration of the script based on the instruction times
        for i in self.instructions:

            if i.start_time < tstart:
                tstart = i.start_time

            if i.stop_time > tstop:
                tstop = i.stop_time
        t = tstop-tstart

        #Reset the values in the instructions
        for i in self.instructions:
            i.done = False
            i.started = False
            new_start_time = i.start_time + t
            new_stop_time = i.stop_time + t
            i.change_vector = 0
            i.to_value = 0

            #print("old start: {} new start: {} old stop: {} new stop:{}. diff: {}".format(i.start_time, new_start_time, i.stop_time, new_stop_time, i.stop_time-i.start_time))
            i.start_time = new_start_time
            i.stop_time = new_stop_time


            i.value = 0
            print(i)

    def __str__(self):
     return "Script: {}. Number of instructions: {}".format(self.name, len(self.instructions))
