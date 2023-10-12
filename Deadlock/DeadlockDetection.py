from Deadlock.SystemInfo import SystemInfo, CustomList


def deadlock_detection():
    input_ways = ['Typing each items', 'Choose a file']
    print('Choose input way\n' + '\n'.join([f'[{i + 1}] {input_way}' for i, input_way in enumerate(input_ways)]))
    input_way_index = 0
    while not (1 <= input_way_index <= 2 or input_way_index is None):
        input_way_index = int(input('Input way (2): ') or 2)

    number_of_processes = 5
    number_of_resource_types = 3
    allocation = [CustomList([0, 1, 0]), CustomList([2, 0, 0]), CustomList([3, 0, 3]), CustomList([2, 1, 1]),
                  CustomList([0, 0, 2])]
    requests = [CustomList([0, 0, 0]), CustomList([2, 0, 2]), CustomList([0, 0, 0]), CustomList([1, 0, 0]),
                CustomList([0, 0, 2])]
    available = CustomList([0, 0, 0])
    if input_way_index == 1:
        number_of_processes = int(input("Number of processes:") or number_of_processes)
        number_of_resource_types = int(input("Number of resource types:") or number_of_resource_types)
        allocation = [CustomList(map(int, input(f"Allocated resources of process {i}:").split() or allocation[i])) for i
                      in range(number_of_processes)]
        requests = [CustomList(map(int, input(f"Requested resources of process {i}:").split() or requests[i])) for i in
                    range(number_of_processes)]
        available = CustomList(map(int, input("Available resources: ").split() or available))
    elif input_way_index == 2:
        file_name = input('[+] Filename (input_deadlock_detection.txt): ')
        with open(file_name or 'input_deadlock_detection.txt', mode='r') as f:
            number_of_processes, number_of_resource_types = list(map(int, f.readline().split()))
            allocation = [CustomList(map(int, f.readline().split())) for _ in range(number_of_processes)]
            requests = [CustomList(map(int, f.readline().split())) for _ in range(number_of_processes)]
            available = CustomList(map(int, f.readline().split()))

    system = SystemInfo(number_of_processes, number_of_resource_types, allocation, available, requests=requests)
    system.print_request()
    print(system.deadlock_detection())



