from queue import PriorityQueue


def vrr(processL: list, eventq: PriorityQueue, quantum: int):
    clock = 0
    cpuIdle = True
    auxq = PriorityQueue()
    while True:
        if auxq.empty():
            print('from eventq')
            if eventq.empty():
                return
            event = eventq.get()
        else:
            print('from auxq')
            event = auxq.get()
        # print(event)
        if event[1] == 'BLOCK':
            if event[0] > clock:
                clock = event[0]
            stuff = processL[event[2]][0]
            time = int(stuff[stuff.find(" ") + 1])

            # adding unblock event to queue
            eventq.put((event[0] + time, 'UNBLOCK', event[2]))
            
            cpuIdle = True
            
            # updating process stuff
            new_stuff = stuff[stuff.find(' ', 3) + 1:]
            processL[event[2]][0] = new_stuff
        elif not cpuIdle:
            eventq.put(event)
            
        elif event[1] == 'ARRIVAL' or event[1] == 'UNBLOCK' or event[1] == 'TIMEOUT':
            if event[0] >= clock:
                clock = event[0]
                processL[event[2]][1][4].append(0)
            else:
                processL[event[2]][1][4].append(clock - event[0])

            # start time
            if event[1] == 'ARRIVAL':
                processL[event[2]][1][2] = clock

            stuff = processL[event[2]][0]
            bursttime = int(stuff[stuff.find(" "):stuff.find(" ", stuff.find(" ") + 1)])
            if bursttime > quantum:
                time = quantum
            else:
                time = bursttime
            clock += time
            # print(time)

            # service time update
            processL[event[2]][1][1] += time

            # updating process stuff
            if bursttime <= quantum:
                new_stuff = stuff[stuff.find(' ', 4) + 1:]
            else:
                new_stuff = 'CPU ' + str(bursttime - quantum) + ' ' + stuff[stuff.find(' ', 4) + 1:]
            processL[event[2]][0] = new_stuff

            if new_stuff == '':
                eventq.put((clock, 'EXIT', event[2]))
                # finish time
                processL[event[2]][1][3] = clock
            else:
                if bursttime <= quantum:
                    # adding block event to aux queue
                    auxq.put((clock, 'BLOCK', event[2]))
                else:
                    # adding timeout to ready queue
                    eventq.put((clock, 'TIMEOUT', event[2]))

        