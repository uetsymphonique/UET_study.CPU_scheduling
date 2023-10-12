from typing import List
from prettytable import PrettyTable


class CustomList(List):
    def __le__(self, other):
        for i in range(min(len(other), len(self))):
            if self[i] > other[i]:
                return False
        return True

    def __sub__(self, other):
        return CustomList([self[i] - other[i] for i in range(min(len(other), len(self)))])

    def __add__(self, other):
        return CustomList([self[i] + other[i] for i in range(min(len(other), len(self)))])

    def __iadd__(self, other):
        return CustomList([self[i] + other[i] for i in range(min(len(other), len(self)))])

    def copy(self):
        arr = super().copy()
        return CustomList(arr)


class SystemInfo:
    def __init__(self, number_of_processes: int, number_of_resource_types: int, allocation: List[CustomList[int]],
                 available: CustomList[int], claim=None, requests=None):
        # print(number_of_processes, number_of_resource_types, available, allocation, claim, sep='\n')
        self._number_of_process = number_of_processes
        self._number_of_resource_types = number_of_resource_types
        self._available = available.copy()
        # print(self._available.__class__)
        self._allocation = allocation.copy()
        if claim is not None:
            self._claim = claim.copy()
            self._need = [self._claim[i] - self._allocation[i] for i in range(number_of_processes)]
        else:
            self._claim = [CustomList([0] * self._number_of_resource_types)] * number_of_processes
            self._need = [CustomList([0] * self._number_of_resource_types)] * number_of_processes
        # print(self._claim)
        # print(self._allocation)
        # print(self._need)
        self._work = available.copy()
        # print(self._work.__class__)
        self._finished = [False] * number_of_processes
        if requests is None:
            self._requests = [CustomList([0] * number_of_resource_types) for _ in range(number_of_processes)]
        else:
            self._requests = requests.copy()
        self._print_banker_table = PrettyTable()
        self._print_banker_table.field_names = ['Process', 'Claim', 'Allocation', 'Need', 'Available', 'New available']
        self._current_state_table = PrettyTable()
        self._current_state_table.field_names = ['Process', 'Claim', 'Allocation', 'Need']
        self._zero_resource_list = CustomList([0] * self._number_of_resource_types)
        self._request_table = PrettyTable()
        self._request_table.field_names = ['Process', 'Request']
        self._print_detection_table = PrettyTable()
        self._print_detection_table.field_names = ['Process', 'Allocation', 'Request', 'Available', 'New available']

    def _find_process_not_finished(self) -> int:
        for i in range(self._number_of_process):
            if not self._finished[i] and self._need[i] < self._work:
                return i

        return -1

    def _find_request_not_finished(self) -> int:
        for i in range(self._number_of_process):
            if self._requests[i] <= self._work and not self._finished[i]:
                return i
        return -1

    def _pretend_allocation(self, i: int):
        # print(f'Before: {self._available}, {self._allocation[i]}, {self._need[i]}')
        self._available = self._available - self._requests[i]
        self._allocation[i] = self._allocation[i] + self._requests[i]
        self._need[i] = self._need[i] - self._requests[i]
        # print(f'After: {self._available}, {self._allocation[i]}, {self._need[i]}')

    def _restore_state(self, i: int):
        self._available = self._available + self._requests[i]
        self._allocation[i] = self._allocation[i] - self._requests[i]
        self._need[i] = self._need[i] + self._requests[i]

    def print_state(self):
        self._current_state_table.clear_rows()
        for i, (claim, allocation, need) in enumerate(zip(self._claim, self._allocation, self._need)):
            self._current_state_table.add_row([i, claim, allocation, need])
        print('Current state of system:', self._current_state_table, f'Available resources: {self._available}\n',
              sep='\n')

    def print_request(self):
        self._request_table.clear_rows()
        for i, request in enumerate(self._requests):
            self._request_table.add_row([i, request])
        print('Current request:', self._request_table, f'Available resources: {self._available}\n', sep='\n')

    def banker_algorithm(self) -> dict:
        self._print_banker_table.clear_rows()
        processes = []
        self._work = self._available.copy()
        self._finished = [False] * self._number_of_process
        process_index = 0
        while process_index >= 0:
            process_index = self._find_process_not_finished()
            if process_index >= 0:
                row_table = [process_index, self._claim[process_index], self._allocation[process_index],
                             self._need[process_index], self._work]
                self._work = self._work + self._allocation[process_index]
                row_table.append(self._work)
                self._print_banker_table.add_row(row_table)
                # self._allocation[process_index] = CustomList([0] * self._number_of_resource_types)
                # print(self._work)
                self._finished[process_index] = True
                processes.append(process_index)

        for i in range(self._number_of_process):
            if not self._finished[i]:
                return {"safe": False, "processes": processes}

        print(f'Banker\'s algorithm:\n {self._print_banker_table}')
        return {"safe": True, "processes": processes}

    def resources_request_algorithm(self, process_index: int, request: CustomList[int]):
        self._requests[process_index] = request
        ret = {"safe": False, "message": "Request accepted!"}
        print(f'Process {process_index} requests {request}')
        self.print_state()

        if self._requests[process_index] <= self._need[process_index]:
            if self._requests[process_index] <= self._available:
                self._pretend_allocation(process_index)
                if not self.banker_algorithm()["safe"]:
                    ret["message"] = 'Request make system enter unsafe state'
                    self._restore_state(process_index)
                else:
                    ret["safe"] = True
                    self._requests[process_index] = CustomList([0] * self._number_of_resource_types)
            else:
                ret["message"] = "Request has exceeded available resources"

        else:
            ret["message"] = 'Request has exceeded the maximum claim'
        return ret

    def deadlock_detection(self):
        self._work = self._available.copy()
        self._finished = [
            False if self._allocation[i] != CustomList([0] * self._number_of_resource_types) or self._requests[
                i] != CustomList([0] * self._number_of_resource_types) else True for i in
            range(self._number_of_process)]

        process_index = 0
        while process_index >= 0:
            process_index = self._find_request_not_finished()
            if process_index >= 0:
                row = [process_index, self._allocation[process_index], self._requests[process_index], self._work]
                self._work = self._work + self._allocation[process_index]
                self._finished[process_index] = True
                self._print_detection_table.add_row(row + [self._work])
        for i in range(self._number_of_process):
            if not self._finished[i]:
                return False
        print("Deadlock Detection:\n", self._print_detection_table)
        return True


if __name__ == "__main__":
    number_of_processes = 5
    number_of_resource_types = 3
    allocation = [CustomList([0, 1, 0]), CustomList([2, 0, 0]), CustomList([3, 0, 2]), CustomList([2, 1, 1]),
                  CustomList([0, 0, 2])]
    claim = [CustomList([7, 5, 3]), CustomList([3, 2, 2]), CustomList([9, 0, 2]), CustomList([2, 2, 2]),
             CustomList([4, 3, 3])]
    available = CustomList([3, 3, 2])
    system = SystemInfo(number_of_processes, number_of_resource_types, allocation, available, claim=claim)
    print(system.banker_algorithm())
    request = CustomList([1, 0, 2])
    processes_index = 1
    print(system.resources_request_algorithm(processes_index, request))
    request = CustomList([3, 3, 0])
    processes_index = 4
    print(system.resources_request_algorithm(processes_index, request))
