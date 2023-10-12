from Deadlock.SystemInfo import SystemInfo, CustomList


def deadlock_avoidance():
    choices = ['Banker\'s algorithm check', 'Resource-Request algorithm']
    print('Choose the demo you want!\n' + '\n'.join(
        [f'[{i + 1}] {c}' for i, c in enumerate(choices)]))
    c = -1
    while not 0 <= c < len(choices):
        c = int(input('Enter your choice (1): ') or 1) - 1

    input_ways = ['Typing each items', 'Choose a file']
    print('Choose input way\n' + '\n'.join([f'[{i + 1}] {input_way}' for i, input_way in enumerate(input_ways)]))
    input_way_index = 0
    while not (1 <= input_way_index <= 2 or input_way_index is None):
        input_way_index = int(input('Input way (2): ') or 2)
    number_of_processes = 5
    number_of_resource_types = 3
    allocation = [CustomList([0, 1, 0]), CustomList([2, 0, 0]), CustomList([3, 0, 2]), CustomList([2, 1, 1]),
                  CustomList([0, 0, 2])]
    claim = [CustomList([7, 5, 3]), CustomList([3, 2, 2]), CustomList([9, 0, 2]), CustomList([2, 2, 2]),
             CustomList([4, 3, 3])]
    available = CustomList([3, 3, 2])
    number_of_requests = 0
    requests = []
    process_indexes = []
    if input_way_index == 1:
        number_of_processes = int(input("Number of processes:") or number_of_processes)
        number_of_resource_types = int(input("Number of resource types:") or number_of_resource_types)
        allocation = [CustomList(map(int, input(f"Allocated resources of process {i}:").split() or allocation[i])) for i in
                      range(number_of_processes)]
        claim = [CustomList(map(int, input(f"Maximum claim resources of process {i}:").split() or claim[i])) for i in
                 range(number_of_processes)]
        available = CustomList(map(int, input("Available resources: ").split() or available))
        if c == 1:
            number_of_requests = int(input("Number of requests:") or number_of_requests)
            for i in range(number_of_requests):
                index = int(input("Process:"))
                process_indexes.append(index)
                requests.append(CustomList(map(int, input(f"Request of process {index}:").split())))
    elif input_way_index == 2:
        file_name = input('[+] Filename (input_deadlock_avoidance.txt): ')
        with open(file_name or 'input_deadlock_avoidance.txt', mode='r') as f:
            number_of_processes, number_of_resource_types = list(map(int, f.readline().split()))
            allocation = [CustomList(map(int, f.readline().split())) for _ in range(number_of_processes)]
            claim = [CustomList(map(int, f.readline().split())) for _ in range(number_of_processes)]
            available = CustomList(map(int, f.readline().split()))
            if c == 1:
                number_of_requests = int(f.readline())
                for i in range(number_of_requests):
                    index = int(f.readline())
                    process_indexes.append(index)
                    requests.append(CustomList(map(int, f.readline().split())))
    system = SystemInfo(number_of_processes, number_of_resource_types, allocation, available, claim=claim)
    system.print_state()
    if c == 0:
        print(system.banker_algorithm())
    if c == 1:
        for (process_index, request) in zip(process_indexes, requests):
            print(system.resources_request_algorithm(process_index, request))


