from typing import List

from prettytable import PrettyTable

from CPU_scheduling.api.process import Process, sort_arrival


def scheduling(processes: List[Process], quantum: int):
    ps = sort_arrival(processes)
    print(ps)
    burst_time = [p.get_burst_time() for p in ps]
    arrival_time = [p.get_arrival_time() for p in ps]

    time_stream = ps[0].get_arrival_time()
    time_str = str(time_stream)
    process_str = '|'
    ps_queue = []
    while len(ps) > 0 or len(ps_queue) > 0:
        while ps and ps[0].get_arrival_time() <= time_stream:
            ps_queue.append(ps.pop(0))
        if len(ps_queue) == 0:
            if time_stream < ps[0].get_arrival_time():
                time_skip = ps[0].get_arrival_time() - time_stream
                time_str += f'{"--" * time_skip}{str(ps[0].get_arrival_time())}'
                process_str += f'{"__" * time_skip}{" " * (len(str(ps[0].get_arrival_time())) - 1)}|'
                time_stream = ps[0].get_arrival_time()
        else:
            process = ps_queue.pop(0)
            time_this_period = min(quantum, process.get_burst_time())
            time_stream = process.preemptive_running(time_stream, time_this_period)
            time_str += f'{"--" * time_this_period}{str(time_stream)}'
            process_str += f'{process.get_name()}{"__" * (time_this_period - len(process.get_name()) + 1)}' \
                           f'{" " * (len(str(time_stream)) - 1)}|'
            while ps and ps[0].get_arrival_time() <= time_stream:
                ps_queue.append(ps.pop(0))
            if process.get_burst_time() > 0:
                ps_queue.append(process)

    print(process_str)
    print(time_str)

    table = PrettyTable()
    table.field_names = Process.get_attributes()
    for i, p in enumerate(sort_arrival(processes)):
        row = p.get_info_in_array()
        table.add_row(row[0:1] + [arrival_time[i], burst_time[i]] + row[3:])
    print(table)

    print(f'Throughput: {len(processes) / time_stream}')
