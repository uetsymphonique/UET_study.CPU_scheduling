from Semaphore.ProducerConsumer import producer_consumer


def semaphore_examples():
    choices = ['Producer-Consumer Problem']
    for i, choice in enumerate(choices):
        print(f'[{i + 1}] {choice}')
    choice_index = -1
    while not 0 <= choice_index < len(choices):
        choice_index = int(input('Enter your choice: ')) - 1
    if choice_index == 0:
        producer_consumer()
