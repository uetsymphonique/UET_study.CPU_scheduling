from typing import List

from prettytable import PrettyTable

from api.process import Process, sort_arrival


def scheduling(processes: List[Process]):
    processes = sort_arrival(processes)
    print(processes)
    time_stream = 0
    time_str = '0'
    process_str = '|'
    for process in processes:
        if time_stream < process.get_arrival_time():
            time_skip = process.get_arrival_time() - time_stream
            time_str += f'{"--" * time_skip}{str(process.get_arrival_time())}'
            process_str += f'{"__" * time_skip}{" " * (len(str(process.get_arrival_time())) - 1)}|'
            time_stream = process.get_arrival_time()
        time_stream = process.nonpreemptive_running(time_stream)
        time_str += f'{"--" * process.get_burst_time()}{str(time_stream)}'
        process_str += f'{process.get_name()}{"__" * (process.get_burst_time() - len(process.get_name()) + 1)}' \
                       f'{" " * (len(str(time_stream)) - 1)}|'

    print(process_str)
    print(time_str)

    table = PrettyTable()
    table.field_names = Process.get_attributes()
    for process in processes:
        table.add_row(process.get_info_in_array())
    print(table)

    print(f'Throughput: {len(processes) / time_stream}')

# running_nonpreemptive(scheduling([Process("p1", 1, 3), Process("p2", 0, 4)]))
