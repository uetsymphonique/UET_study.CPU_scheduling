from Deadlock.DeadlockDetection import deadlock_detection
from Deadlock.DeadlockAvoidance import deadlock_avoidance


def deadlock_examples():
    choices = ['Deadlock Avoidance', 'Deadloclk Detection']
    for i, choice in enumerate(choices):
        print(f'[{i + 1}] {choice}')
    choice_index = -1
    while not 0 <= choice_index < len(choices):
        choice_index = int(input('Enter your choice: ')) - 1
    if choice_index == 0:
        deadlock_avoidance()
    elif choice_index == 1:
        deadlock_detection()
