from queue import PriorityQueue

def hrrn(processL: list, eventq: PriorityQueue):
    clock = 0
    readyL = []
    cpuIdle = True
    while True:
        if eventq.empty():
            return
        event = eventq.get()
        print(event)

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
            
            readyL.append((event[2], time))

        elif event[1] == 'BLOCK':
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
        
        elif event[1] == 'EXIT':
            if event[0] > clock:
                clock = event[0]
            cpuIdle = True
        
        if cpuIdle and len(readyL) > 0:
            cpuIdle = False
            maxR = 0
            for i in readyL:
                ratio = (clock - processL[i[0]][1][2] + i[1]) / i[1]
                if ratio > maxR:
                    maxId = i[0]
                    maxR = ratio
                    time = i[1]
            
            stuff = processL[maxId][0]
            new_stuff = stuff[stuff.find(' ', 4)+1:]
            processL[maxId][0] = new_stuff
            if new_stuff == '':
                eventq.put((clock + time, 'EXIT', maxId))
                # finish time
                processL[event[2]][1][3] = clock
            else:
                eventq.put((clock + time, 'BLOCK', maxId))
            readyL.remove((maxId, time))
            print("dispatched " + str(maxId))
            
