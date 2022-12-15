from queue import PriorityQueue


def fcfs(processL: list, eventq: PriorityQueue):
    clock = 0
    while True:
        if eventq.empty():
            return
        event = eventq.get()
        #print(event)

        if event[1] == 'ARRIVAL' or event[1] == 'UNBLOCK':
            if event[0] >= clock:
                clock = event[0]
                processL[event[2]][1][4].append(0)
            else:
                processL[event[2]][1][4].append(clock - event[0])

            #arrival time
            if event[1] == 'ARRIVAL':
                processL[event[2]][1][2] = clock

            stuff = processL[event[2]][0]
            time = int(stuff[stuff.find(" "):stuff.find(" ", stuff.find(" ") + 1)])

            clock += time
            #print(time)

            # service time update
            processL[event[2]][1][1] += time

            #updating process stuff
            new_stuff = stuff[stuff.find(' ', 4)+1:]
            processL[event[2]][0] = new_stuff

            if new_stuff == '':
                eventq.put((clock, 'EXIT', event[2]))
                # finish time
                processL[event[2]][1][3] = clock
            else:
                # adding block event to queue
                eventq.put((clock, 'BLOCK', event[2]))

        elif event[1] == 'BLOCK':
            if event[0] > clock:
                clock = event[0]
            stuff = processL[event[2]][0]
            time = int(stuff[stuff.find(" ") + 1])

            # adding unblock event to queue
            eventq.put((event[0] + time, 'UNBLOCK', event[2]))

            # updating process stuff
            new_stuff = stuff[stuff.find(' ', 3) + 1:]
            processL[event[2]][0] = new_stuff

