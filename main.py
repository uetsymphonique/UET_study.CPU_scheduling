from CPU_scheduling.CPU_scheduling import cpu_scheduling
from Semaphore.Semaphore import semaphore_examples
from Deadlock.Deadlock import deadlock_examples
if __name__ == "__main__":
    choices = ['CPU scheduling algorithms', 'Semaphore examples', "Deadlock examples"]
    while True:
        for i, choice in enumerate(choices):
            print(f'[{i+1}] {choice}')
        choice_index = -1
        while not 0 <= choice_index < len(choices):
            choice_index = int(input('Enter your choice: ')) - 1
        if choice_index == 0:
            cpu_scheduling()
        elif choice_index == 1:
            semaphore_examples()
        elif choice_index == 2:
            deadlock_examples()
        if (input('Exit y/n? (n): ') or 'n') == 'y':
            break

