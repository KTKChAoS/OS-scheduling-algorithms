from queue import PriorityQueue, Queue
import copy


def feedback(processL: list, eventq: PriorityQueue, quantum: int, num_priorities: int):
    clock = 0
    cpuIdle = True

    tempq = copy.copy(eventq)
    eventq = PriorityQueue()

    while not tempq.empty():
        event = tempq.get()
        event += (0,)
        eventq.put(event)

    # feedQ will be list of queues, and the q will contain pid
    feedQ = []
    for i in range(0, num_priorities):
        feedQ.append(Queue())

    while True:
        if eventq.empty():
            return
        event = eventq.get()
        # print(event)

        if event[1] == 'ARRIVAL' or event[1] == 'UNBLOCK':
            if event[0] >= clock:
                clock = event[0]

            # priority doesn't change as it wasn't timed out
            if event[1] == 'ARRIVAL':
                # print("here for ", event[2], event[1])
                feedQ[0].put(event[2])
            else:
                feedQ[event[3]].put(event[2])

            # subtracting cur time from resp. sum
            processL[event[2]][1][4] -= clock

        elif event[1] == 'TIMEOUT':
            if event[0] >= clock:
                clock = event[0]
            cpuIdle = True
            processL[event[2]][1][4] -= clock
            if event[3] == (num_priorities - 1):
                feedQ[num_priorities - 1].put(event[2])
            else:
                feedQ[event[3]+1].put(event[2])

        elif event[1] == 'BLOCK':
            if event[0] > clock:
                clock = event[0]
            stuff = processL[event[2]][0]
            time = int(stuff[stuff.find(" "):stuff.find(" ", stuff.find(" ") + 1)])

            # adding unblock event to queue
            eventq.put((clock + time, 'UNBLOCK', event[2], event[3]))

            cpuIdle = True

            # updating process stuff
            new_stuff = stuff[stuff.find(' ', 3) + 1:]
            processL[event[2]][0] = new_stuff

        elif event[1] == 'EXIT':
            if event[0] >= clock:
                clock = event[0]
            cpuIdle = True
            # finish time
            processL[event[2]][1][3] = clock

        if cpuIdle:
            flag = False
            pid, i = -1, -1
            for i in range(0, len(feedQ)):
                if not feedQ[i].empty():
                    pid = feedQ[i].get()
                    break
                elif i == len(feedQ) - 1:
                    flag = True
            if flag:
                continue

            # setting start time
            if processL[pid][2]:
                processL[pid][1][2] = clock
                processL[pid][2] = False
            # adding current clock to resp. sum
            processL[pid][1][4] += clock
            processL[pid][1][5] += 1

            cpuIdle = False
            stuff = processL[pid][0]
            bursttime = int(stuff[stuff.find(" "):stuff.find(" ", stuff.find(" ") + 1)])
            if bursttime > quantum:
                time = quantum
            else:
                time = bursttime

            # service time update
            processL[pid][1][1] += time

            # updating process stuff
            if bursttime <= quantum:
                new_stuff = stuff[stuff.find(' ', 4) + 1:]
            else:
                new_stuff = 'CPU ' + str(bursttime - quantum) + ' ' + stuff[stuff.find(' ', 4) + 1:]
            processL[pid][0] = new_stuff

            if new_stuff == '':
                eventq.put((clock + time, 'EXIT', pid))

            else:
                if bursttime <= quantum:
                    # adding block event to aux queue
                    eventq.put(((clock + time), 'BLOCK', pid, i))

                else:
                    # adding timeout to ready queue
                    eventq.put((clock + quantum, 'TIMEOUT', pid, i))
