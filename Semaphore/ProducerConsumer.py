from threading import Thread, Semaphore
import time

"""Shared resources"""
capacity = 10
buffer = [-1] * capacity
produced_index = 0
consumed_index = 0
produced_limit = 20
consumed_limit = 20

"""Semaphores"""
# mutex semaphore is used to avoid conflicts between 2 processes
mutex = Semaphore(1)
# empty semaphore is used for Producer process
empty = Semaphore(capacity)
# full semaphore is used for Consumer process
full = Semaphore(0)

"""Producer"""


class Producer(Thread):

    def run(self):
        global capacity, buffer, produced_index, consumed_index
        global mutex, empty, full

        produced_items = 0
        counter = 0

        while produced_items < produced_limit:
            empty.acquire()
            mutex.acquire()

            counter += 1
            buffer[produced_index] = counter
            produced_index = (produced_index + 1) % capacity
            print(f'Produce items: {counter}')

            mutex.release()
            full.release()

            time.sleep(1)

            produced_items += 1


"""Consumer"""


class Consumer(Thread):

    def run(self):
        global capacity, buffer, produced_index, consumed_index
        global mutex, empty, full

        consumed_items = 0

        while consumed_items < consumed_limit:
            full.acquire()
            mutex.acquire()

            item = buffer[consumed_index]
            consumed_index = (consumed_index + 1) % capacity
            print(f'Consume item: {item}')

            mutex.release()
            empty.release()

            time.sleep(2.5)

            consumed_items += 1


def producer_consumer():
    global capacity, buffer, produced_index, consumed_index, produced_limit, consumed_limit
    global mutex, empty, full

    capacity = int(input(f'[-] Capacity of buffer ({capacity}): ') or capacity)
    produced_limit = int(input(f'[-] Produced limit ({produced_limit}): ') or produced_limit)
    consumed_limit = int(input(f'[-] Consumed limit ({consumed_limit}): ') or consumed_limit)
    print('[+] Example for Producer-Consumer Problem')
    producer = Producer()
    consumer = Consumer()

    consumer.start()
    producer.start()

    producer.join()
    consumer.join()


if __name__ == '__main__':
    producer_consumer()
