from typing import List


class Process:
    def __init__(self, name, arrival_time=0, burst_time=1):
        self.__name = name
        self.__arrival_time = arrival_time
        self.__recent_time_in_queue = arrival_time
        self.__burst_time = burst_time
        self.__turnaround_time = -1
        self.__waiting_time = 0
        self.__response_time = -1

    def nonpreemptive_running(self, time_stream):
        self.__waiting_time = time_stream - self.__arrival_time
        time_stream += self.__burst_time
        self.__response_time = self.__turnaround_time = time_stream - self.__arrival_time
        return time_stream

    def preemptive_running(self, time_stream, time_this_period):
        if self.__recent_time_in_queue == self.__arrival_time:
            self.__response_time = time_stream - self.__arrival_time
        self.__waiting_time += time_stream - self.__recent_time_in_queue
        self.__burst_time -= time_this_period
        time_stream += time_this_period
        self.__recent_time_in_queue = time_stream
        if self.__burst_time <= 0:
            self.__turnaround_time = time_stream - self.__arrival_time
        return time_stream

    def get_info_in_array(self):
        return [self.__name, self.__arrival_time, self.__burst_time, self.__turnaround_time, self.__waiting_time,
                self.__response_time]

    def __lt__(self, other):
        return self.__burst_time < other.get_burst_time() \
            or (self.__burst_time == other.get_burst_time() and self.__arrival_time < other.get_burst_time())

    def __gt__(self, other):
        return self.__burst_time > other.get_burst_time() \
            or (self.__burst_time == other.get_burst_time() and self.__arrival_time > other.get_burst_time())

    def __str__(self):
        return f'Process({self.__name}, {self.__arrival_time}, {self.__burst_time})'

    def __repr__(self):
        return f'Process({self.__name}, {self.__arrival_time}, {self.__burst_time})'

    @staticmethod
    def get_attributes():
        return ["name", "arrival_time", "burst_time", "turnaround_time", "waiting_time", "response_time"]

    def get_name(self):
        return self.__name

    def get_arrival_time(self):
        return self.__arrival_time

    def get_recent_time_in_queue(self):
        return self.__recent_time_in_queue

    def get_burst_time(self):
        return self.__burst_time

    def get_turnaround_time(self):
        return self.__turnaround_time

    def get_waiting_time(self):
        return self.__waiting_time

    def get_response_time(self):
        return self.__response_time

    def set_name(self, name):
        self.__name = name

    def set_arrival_time(self, arrival_time):
        self.__arrival_time = arrival_time

    def set_recent_time_in_queue(self, recent_time_in_queue):
        self.__recent_time_in_queue = recent_time_in_queue

    def set_burst_time(self, burst_time):
        self.__burst_time = burst_time

    def set_turnaround_time(self, turnaround_time):
        self.__turnaround_time = turnaround_time

    def set_waiting_time(self, waiting_time):
        self.__waiting_time = waiting_time

    def set_response_time(self, response_time):
        self.__response_time = response_time


def sort_arrival(processes: List[Process]) -> List[Process]:
    return sorted(processes, key=lambda process: process.get_arrival_time())
