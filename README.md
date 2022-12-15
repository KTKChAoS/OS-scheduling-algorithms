# OS-scheduling-algorithms
Project 3 of OS class - scheduling algorithms in python
Files:
  1. main.py - the main file. It reads in the pfile and sfile, initializes event queue and calls the required scheduling algorithm
  2. fcfs.py, vrr.py, hrrn.py, feedback.py, srt.py - the scheduling algorithms
  3. pfile - the process file. Contains arrival time and activity
  4. sfile - the scheduler file, containing what scheduling algorithm to use

How to compile and run:
	make sure the files are all in the same directory, and just call 'python3 main.py' if using command line.

Notes
	I have assumed that process always starts and ends in CPU activity, since none of the examples shown end in IO, and the EXIT event in the prompt states that process is running on CPU.
