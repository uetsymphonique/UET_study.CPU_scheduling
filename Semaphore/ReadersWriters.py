import random
from threading import Thread, Semaphore
import time

# data_set is shared among a number of concurrent process
data_set = []
# read_count: int (initialize = 0) count the number of readers are reading
read_count = 0

# semaphore wrt (initialize = 1) used to manage write access
# semaphore mutex (initialize = 1) used to manage read_count access
wrt = Semaphore(1)
mutex = Semaphore(1)

read_limit = 10
write_limit = 5

write_times = 0
read_times = 0


class Writer(Thread):
    def run(self):
        global wrt, write_limit, data_set, write_times

        while write_times < write_limit:
            wrt.acquire()
            print(f'Writing... by {self.__repr__()}')
            data_set.append('Data')
            write_times += 1
            wrt.release()

            time.sleep(3)


class Reader(Thread):
    def run(self):
        global wrt, read_limit, read_count, data_set, read_times

        while read_times < read_limit:
            mutex.acquire()
            read_count += 1
            if read_count == 1:
                wrt.acquire()
            mutex.release()
            print(f'Reading... by {self.__repr__()}, now have ({read_count}) readers')
            print(f'Data_set: {data_set}')
            read_times += 1
            mutex.acquire()
            read_count -= 1
            if read_count == 0:
                wrt.release()
            mutex.release()

            time.sleep(10)


def reader_writer():
    random_choice = ''
    num_of_writers = 2
    num_of_readers = 4
    while random_choice not in ('y', 'n'):
        random_choice = input('Customize the reader and writer(y/n)? (n):').lower() or 'n'
    choices = []

    if random_choice == 'n':
        num_of_writers = int(input(f'[+] Numbers of writers ({num_of_writers}): ') or num_of_writers)
        num_of_readers = int(input(f'[+] Numbers of readers ({num_of_readers}): ') or num_of_readers)
        writers = ['wr' for _ in range(num_of_writers)]
        readers = ['rd' for _ in range(num_of_readers)]
        choices = writers + readers
        random.shuffle(choices)
    else:
        input_ways = ['Typing each thread', 'Choose a file']
        print('Choose your input way\n' + '\n'.join([f'[{i + 1}] '
                                                     f'{input_way}' for i, input_way in enumerate(input_ways)]))
        input_way_index = 0
        while not (1 <= input_way_index <= 2 or input_way_index is None):
            input_way_index = int(input('Input way (2): ') or 2)

        def check_inp(arr):
            for a in arr:
                if a not in ['wr', 'rd']:
                    return False
            return True

        if input_way_index == 1:
            while not check_inp(choices):
                str_input = input('[+] Typing threads (wr wr rd rd rd rd): ') or 'wr wr rd rd rd rd'
                choices = str_input.split(' ')
        else:
            file_name = input('[+] Filename (input_producer_consumer.txt): ')
            try:
                with open(file_name or 'input_producer_consumer.txt', mode='r') as f:
                    line = f.readline()
                    choices = line.split(' ')
                    if not check_inp(choices):
                        raise ValueError('Invalid input!')
            except Exception as err:
                print(err)

    threads = [Writer() if choice == 'wr' else Reader() for choice in choices]

    print(choices)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    reader_writer()
