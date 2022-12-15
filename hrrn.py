from queue import PriorityQueue


def hrrn(processL: list, eventq: PriorityQueue, service_given: bool, alpha: float):
    clock = 0
    readyL = []
    cpuIdle = True
    serviceTimes = []
    for x in range(0, len(processL)):
        serviceTimes.append([])
    while True:
        if eventq.empty():
            # calculating service time
            if service_given:
                for i in range(0, len(processL)):
                    results = [0.0] * len(serviceTimes[i])
                    results[0] = serviceTimes[i][0]
                    for t in range(1, len(serviceTimes[i])):
                        results[t] = alpha * serviceTimes[i][t] + (1 - alpha) * results[t-1]
                    serviceTimes[i] = results
            for i in range(0, len(processL)):
                processL[i][1][1] = sum(serviceTimes[i])
            return
        event = eventq.get()
        # print(event)

        if event[1] == 'ARRIVAL' or event[1] == 'UNBLOCK':
            if event[0] > clock:
                clock = event[0]
            else:
                processL[event[2]][1][4] += (clock - event[0])
            processL[event[2]][1][5] += 1

            stuff = processL[event[2]][0]
            time = int(stuff[stuff.find(" "):stuff.find(" ", stuff.find(" ") + 1)])

            readyL.append((event[2], time))

        elif event[1] == 'BLOCK':
            if event[0] > clock:
                clock = event[0]
            stuff = processL[event[2]][0]
            time = int(stuff[stuff.find(" "):stuff.find(" ", stuff.find(" ") + 1)])

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
            # finish time
            processL[event[2]][1][3] = clock

        if cpuIdle and len(readyL) > 0:
            cpuIdle = False
            maxId, maxR, time = -1, 0, -1
            for i in readyL:
                ratio = (clock - processL[i[0]][1][0] + i[1]) / i[1]
                if ratio > maxR:
                    maxId = i[0]
                    maxR = ratio
                    time = i[1]

            stuff = processL[maxId][0]
            new_stuff = stuff[stuff.find(' ', 4) + 1:]
            processL[maxId][0] = new_stuff
            if new_stuff == '':
                eventq.put((clock + time, 'EXIT', maxId))
            else:
                eventq.put((clock + time, 'BLOCK', maxId))
            readyL.remove((maxId, time))

            if processL[maxId][2]:
                processL[maxId][1][2] = clock
                processL[maxId][2] = False

            clock += time
            # append service time
            serviceTimes[maxId].append(time)
            # print("dispatched " + str(maxId))
