from queue import PriorityQueue

from fcfs import fcfs
from feedback import feedback
from hrrn import hrrn
from srt import srt
from vrr import vrr

if __name__ == '__main__':

    processL = []
    file1 = open("pfile", "r")

    for line in file1:
        arrT = int(line[:line.find(" ")])

        # process, arrival time, service time, start time, finish time, response time sum, times in q
        temp = [line.strip()[line.find(" ")+1:]+' ', [arrT, 0, 0, 0, 0, 0], True]
        processL.append(temp)
    file1.close()
    # processL[0][1][4].append(0)
    # print(processL)

    # creating priority queue for events and adding in all arrival events
    eventq = PriorityQueue()
    q = 0
    for r in processL:
        eventq.put((r[1][0], "ARRIVAL", q))
        q += 1

    file2 = open("sfile", "r")
    algo = file2.readline().strip()

    # FCFS
    if algo.lower() == 'fcfs':
        print("Using First Come First Serve algorithm")
        fcfs(processL, eventq)

    # VRR
    elif algo.lower() == 'vrr':
        print("Using Virtual Round Robin algorithm")
        temp = file2.readline().strip()
        quantum = int(temp[temp.find('=')+1:])
        vrr(processL, eventq, quantum)

    # SRT
    elif algo.lower() == 'srt':
        print("Using Shortest Remaining Time algorithm")
        temp = file2.readline().strip()
        service_given = False
        alpha = 0
        if temp[0] == 's':
            if temp[temp.find('=') + 1].lower() == 't':
                service_given = True
        else:
            alpha = float(temp[temp.find('=')+1:])
        temp = file2.readline().strip()
        if temp[0] == 'a':
            alpha = float(temp[temp.find('=') + 1:])
        else:
            if temp[temp.find('=') + 1].lower() == 't':
                service_given = True
        srt(processL, eventq, service_given, alpha)

    # HRRN
    elif algo.lower() == 'hrrn':
        print("Using Highest Response Ratio Next algorithm")
        temp = file2.readline().strip()
        service_given = False
        alpha = 0
        if temp[0] == 's':
            if temp[temp.find('=')+1].lower() == 't':
                service_given = True
        else:
            alpha = float(temp[temp.find('=')+1:])
        temp = file2.readline().strip()
        if temp[0] == 'a':
            alpha = float(temp[temp.find('=') + 1:])
        else:
            if temp[temp.find('=')+1].lower() == 't':
                service_given = True
        hrrn(processL, eventq, service_given, alpha)

    # FEEDBACK
    elif algo.lower() == 'feedback':
        print("Using Feedback algorithm")
        temp = file2.readline().strip()
        quantum = 0
        num_priorities = 0
        if temp[0] == 'q':
            quantum = int(temp[temp.find('=')+1:])
        else:
            num_priorities = int(temp[temp.find('=')+1:])
        temp = file2.readline().strip()
        if temp[0] == 'n':
            num_priorities = int(temp[temp.find('=') + 1:])
        else:
            quantum = bool(temp[temp.find('=') + 1:])
        feedback(processL, eventq, quantum, num_priorities)

    else:
        print("whoops! something went wrong. Check the first line of scheduler file")

    # while not eventq.empty():
    #     print(eventq.get())

    file2.close()

    # printing the info
    i = 0
    mtat, mntat, mrt = 0, 0, 0
    for r in processL:
        print("Process ", str(i))
        print("\tArrival Time: ", r[1][0])
        print("\tService Time: ", round(r[1][1], 3))
        print("\tStart Time: ", r[1][2])
        print("\tFinish Time: ", r[1][3])
        tat = r[1][3] - r[1][0]
        mtat += tat
        print("\tTurnaround Time: ", tat)
        ntat = tat/r[1][1]
        mntat += ntat
        print("\tNorm. Turn. Time Time: ", round(ntat, 3))
        if r[1][4] == 0:
            rt = 0
        else:
            rt = (r[1][4])/(r[1][5])
        mrt += rt
        print("\tAvg. resp. time Time: ", round(rt, 3))
        print("---------------------------------------")
        i += 1
    print("Mean Turnaround: ", round(mtat/i, 2))
    print("Mean Norm. Turnaround: ", round(mntat/i, 2))
    print("Mean Resp. Time: ", round(mrt/i, 2))
