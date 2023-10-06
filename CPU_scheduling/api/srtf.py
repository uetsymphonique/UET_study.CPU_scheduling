from typing import List

from prettytable import PrettyTable

from CPU_scheduling.api.process import Process, sort_arrival
from CPU_scheduling.ds.minHeapImpByArray import MinHeapTree


def scheduling(processes: List[Process]):
    ps = sort_arrival(processes)
    print(ps)
    burst_time = [p.get_burst_time() for p in ps]
    arrival_time = [p.get_arrival_time() for p in ps]

    ps_queue = MinHeapTree(len(processes), Process('inf', 0, -1), Process('dump', 0, -1))
    time_stream = ps[0].get_arrival_time()
    time_str = str(time_stream)
    process_str = '|'
    while len(ps) > 0 or ps_queue.get_size() > 0:
        while ps and ps[0].get_arrival_time() == time_stream:
            ps_queue.insert(ps.pop(0))
        if ps_queue.get_size() == 0:
            if time_stream < ps[0].get_arrival_time():
                time_skip = ps[0].get_arrival_time() - time_stream
                time_str += f'{"--" * time_skip}{str(ps[0].get_arrival_time())}'
                process_str += f'{"__" * time_skip}{" " * (len(str(ps[0].get_arrival_time())) - 1)}|'
                time_stream = ps[0].get_arrival_time()
        else:
            process = ps_queue.get_pop()
            time_this_period = min(ps[0].get_arrival_time() - time_stream,
                                   process.get_burst_time()) if ps else process.get_burst_time()
            time_stream = process.preemptive_running(time_stream, time_this_period)
            time_str += f'{"--" * time_this_period}{str(time_stream)}'
            process_str += f'{process.get_name()}{"__" * (time_this_period - len(process.get_name()) + 1)}{" " * (len(str(time_stream)) - 1)}|'
            if process.get_burst_time() <= 0:
                ps_queue.remove()

    print(process_str)
    print(time_str)

    table = PrettyTable()
    table.field_names = Process.get_attributes()
    for i, p in enumerate(sort_arrival(processes)):
        row = p.get_info_in_array()
        table.add_row(row[0:1] + [arrival_time[i], burst_time[i]] + row[3:])
    print(table)

    print(f'Throughput: {len(processes)/time_stream}')
