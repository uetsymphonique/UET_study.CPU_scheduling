from CPU_scheduling.api import fcfs, srtf, nsjf, rr
from CPU_scheduling.api.process import Process


def cpu_scheduling():
    input_ways = ['Typing each process', 'Choose a file']
    print('Choose your input way\n' + '\n'.join([f'[{i + 1}] {input_way}' for i, input_way in enumerate(input_ways)]))
    input_way_index = 0
    while not (1 <= input_way_index <= 2 or input_way_index is None):
        input_way_index = int(input('Input way (2): ') or 2)
    processes = []

    if input_way_index == 1:
        num_of_processes = int(input("[+] Number of process: "))
        for i in range(num_of_processes):
            a = int(input(f'[+] Process {i + 1}: arrival time '))
            b = int(input(f'[+] Process {i + 1}: burst time   '))
            processes.append(Process(f'P{i}', a, b))
    elif input_way_index == 2:
        file_name = input('[+] Filename (input_cpu_scheduling.txt): ')
        try:
            with open(file_name or 'input_cpu_scheduling.txt', mode='r') as f:
                lines = f.readlines()
                num_of_processes = int(lines[0])
                for i in range(num_of_processes):
                    a, b = list(lines[i + 1].split())
                    processes.append(Process(f'P{i + 1}', int(a), int(b)))
        except Exception as err:
            print(err)

    choices = ['FCFS - First Come First Served', 'NSJF - Nonpreemptive Shortest Job First',
               'SRTF - Shortest Remaining Time First(preemptive SJF)', 'RR - Round Robin']
    print(
        'Choose the CPU scheduling algorithm you want!\n' + '\n'.join(
            [f'[{i + 1}] {choice}' for i, choice in enumerate(choices)]))

    choice_index = 0
    while not (1 <= choice_index <= len(choices)):
        choice_index = int(input('Algorithm (type number): '))

    if choice_index == 1:
        fcfs.scheduling(processes)
    elif choice_index == 2:
        nsjf.scheduling(processes)
    elif choice_index == 3:
        srtf.scheduling(processes)
    elif choice_index == 4:
        quantum = int(input('[-] Quantum q: '))
        rr.scheduling(processes, quantum)
