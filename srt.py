from queue import PriorityQueue


def srt(processL: list, eventq: PriorityQueue, service_given: bool, alpha: float):
    clock = 0
    # contains (pid, bursttime remaining)
    readyq = []
    serviceTimes = []
    for x in range(0, len(processL)):
        serviceTimes.append([])

    # pid, time it started, time it should end
    class C:
        pid: int
        startT: int
        endT: int

        def __init__(self, pid=-1, startT=-1, endT=-1):
            self.pid = pid
            self.startT = startT
            self.endT = endT


    if eventq.empty():
        return
    event = eventq.get()
    # print(event)
    if event[0] >= clock:
        clock = event[0]
    # start time for the first event
    processL[event[2]][1][2] = clock

    stuff = processL[event[2]][0]
    totNewTime = int(stuff[stuff.find(" "):stuff.find(" ", stuff.find(" ") + 1)])
    serviceTimes[event[2]].append(totNewTime)
    currP = C(event[2], clock, clock + totNewTime)
    eventq.put((currP.endT, 'BLOCK', currP.pid))
    cpuIdle = False

    while True:
        if eventq.empty():
            if len(readyq) == 0:
                # calculating service time
                if service_given:
                    for i in range(0, len(processL)):
                        results = [0.0] * len(serviceTimes[i])
                        results[0] = serviceTimes[i][0]
                        for t in range(1, len(serviceTimes[i])):
                            results[t] = alpha * serviceTimes[i][t] + (1 - alpha) * results[t - 1]
                        serviceTimes[i] = results
                for i in range(0, len(processL)):
                    processL[i][1][1] = sum(serviceTimes[i])
                return
            else:
                eventq.put((clock + currP.endT - currP.startT, 'EXIT', currP.pid))
        event = eventq.get()
        # print(event)

        if event[1] == 'ARRIVAL' or event[1] == 'UNBLOCK':
            if event[0] >= clock:
                clock = event[0]

            stuff = processL[event[2]][0]
            totNewTime = int(stuff[stuff.find(" "):stuff.find(" ", stuff.find(" ") + 1)])
            serviceTimes[event[2]].append(totNewTime)
            currTime = currP.endT - clock
            if currTime > totNewTime:
                # need to swap out
                # print(str(currP.pid) + ' swapped for ' + str(event[2]))
                readyq.append((currP.pid, currTime, clock))

                # increment number of times in ready q
                processL[currP.pid][1][5] += 1

                stuff = processL[currP.pid][0]
                new_stuff = 'CPU ' + str(currTime) + ' ' + stuff[stuff.find(' ', 4) + 1:]
                processL[currP.pid][0] = new_stuff
                currP = C(event[2], clock, clock + totNewTime)
                eventq.put((currP.endT, 'BLOCK', currP.pid))
                # response time
                processL[currP.pid][1][4] += clock - event[0]

            else:
                readyq.append((event[2], totNewTime, clock))
                # increment number of times in ready q
                processL[currP.pid][1][5] += 1

            # subtracting cur time from resp. sum
            # processL[event[2]][1][4] -= clock

        elif event[1] == 'BLOCK':
            stuff = processL[event[2]][0]
            if currP.pid != event[2] or event[0] != currP.endT:
                continue
            new_stuff = stuff[stuff.find(' ', 4) + 1:]
            processL[event[2]][0] = new_stuff
            if event[0] > clock:
                clock = event[0]
            if new_stuff == '':
                eventq.put((clock, 'EXIT', event[2]))
                continue
            stuff = new_stuff
            time = int(stuff[stuff.find(" "):stuff.find(" ", stuff.find(" ") + 1)])

            # adding unblock event to queue
            eventq.put((clock + time, 'UNBLOCK', event[2]))
            # updating process stuff
            new_stuff = stuff[stuff.find(' ', 3) + 1:]
            processL[event[2]][0] = new_stuff
            cpuIdle = True

        elif event[1] == 'EXIT':
            if event[0] >= clock:
                clock = event[0]
            # finish time
            processL[event[2]][1][3] = clock
            cpuIdle = True

        if cpuIdle:
            if len(readyq) == 0:
                continue
            cpuIdle = False
            minT, minTid, ct = float('inf'), float('inf'), -1
            for i in readyq:
                if i[1] < minT:
                    minT = i[1]
                    minTid = i[0]
                    ct = i[2]

            readyq.remove((minTid, minT, ct))
            nxtP = int(minTid)
            stuff = processL[nxtP][0]
            totNewTime = int(stuff[stuff.find(" "):stuff.find(" ", stuff.find(" ") + 1)])
            currP = C(nxtP, clock, clock + totNewTime)
            eventq.put((currP.endT, 'BLOCK', currP.pid))

            processL[currP.pid][1][4] += clock - ct
