from typing import List

from prettytable import PrettyTable

from api.process import Process, sort_arrival
from ds.minHeapImpByArray import MinHeapTree


def scheduling(processes: List[Process]):
    ps = sort_arrival(processes)
    print(ps)
    ps_queue = MinHeapTree(len(processes), Process('inf', 0, -1), Process('dump', 0, -1))
    time_stream = ps[0].get_arrival_time()
    time_str = str(time_stream)
    process_str = '|'
    while len(ps) > 0 or ps_queue.get_size() > 0:
        while ps and ps[0].get_arrival_time() <= time_stream:
            ps_queue.insert(ps.pop(0))
        if ps_queue.get_size() == 0:
            if time_stream < ps[0].get_arrival_time():
                time_skip = ps[0].get_arrival_time() - time_stream
                time_str += f'{"--" * time_skip}{str(ps[0].get_arrival_time())}'
                process_str += f'{"__" * time_skip}{" " * (len(str(ps[0].get_arrival_time())) - 1)}|'
                time_stream = ps[0].get_arrival_time()
        else:
            process = ps_queue.get_pop()
            time_stream = process.nonpreemptive_running(time_stream)
            time_str += f'{"--" * process.get_burst_time()}{str(time_stream)}'
            process_str += f'{process.get_name()}{"__" * (process.get_burst_time() - len(process.get_name()) + 1)}' \
                           f'{" " * (len(str(time_stream)) - 1)}|'
            ps_queue.remove()

    print(process_str)
    print(time_str)

    table = PrettyTable()
    table.field_names = Process.get_attributes()
    for process in processes:
        table.add_row(process.get_info_in_array())
    print(table)

    print(f'Throughput: {len(processes) / time_stream}')
