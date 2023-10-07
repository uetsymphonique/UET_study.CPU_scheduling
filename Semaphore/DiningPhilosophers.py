from threading import Thread, Semaphore
import time
import random

num_of_philosophers = 5
num_of_chopsticks = num_of_philosophers
visualization_array = []
for i in range(num_of_philosophers):
    visualization_array += [' ', f'P{i}', ' ', '|']

chopsticks = [Semaphore(1) for _ in range(num_of_chopsticks)]

eating_limit = 3


class Philosopher(Thread):
    def __init__(self, index):
        super().__init__()
        self._index = index

    def run(self):
        eating_times = 0
        global chopsticks, eating_limit, visualization_array
        while eating_times < eating_limit:
            print(f'Philosopher {self._index} is thinking({"".join(visualization_array)})\n')
            time.sleep(random.randint(1, 5))
            # time.sleep(1.5)

            left_chopsticks_index = self._index
            right_chopsticks_index = (self._index + 1) % num_of_chopsticks

            chopsticks[left_chopsticks_index].acquire()
            chopsticks[right_chopsticks_index].acquire()

            left_position = self._index * 4
            left_chopsticks_position = left_position - 1
            right_position = left_position + 2
            right_chopsticks_position = right_position + 1

            visualization_array[left_position], visualization_array[left_chopsticks_position] = \
                visualization_array[left_chopsticks_position], visualization_array[left_position]

            visualization_array[right_position], visualization_array[right_chopsticks_position] = \
                visualization_array[right_chopsticks_position], visualization_array[right_position]

            print(f'Philosopher {self._index} is eating  ({"".join(visualization_array)})\n')
            eating_times += 1
            time.sleep(random.randint(1, 5))
            # time.sleep(1.5)

            visualization_array[left_position], visualization_array[left_chopsticks_position] = \
                visualization_array[left_chopsticks_position], visualization_array[left_position]

            visualization_array[right_position], visualization_array[right_chopsticks_position] = \
                visualization_array[right_chopsticks_position], visualization_array[right_position]

            chopsticks[left_chopsticks_index].release()
            chopsticks[right_chopsticks_index].release()


def dining_philosophers():
    global num_of_philosophers, num_of_chopsticks, eating_limit
    num_of_philosophers = int(input(f'Number of philosophers ({num_of_philosophers}): ') or num_of_philosophers)
    num_of_chopsticks = num_of_philosophers
    eating_limit = int(input(f'Eating limit ({eating_limit})') or eating_limit)
    philosophers = [Philosopher(i) for i in range(num_of_philosophers)]

    for philosopher in philosophers:
        philosopher.start()

    for philosopher in philosophers:
        philosopher.join()


if __name__ == '__main__':
    dining_philosophers()
