import sys

try:
    X = int(input('X: '))
    Y = int(input('Y: '))
except ValueError:
    print('Please type a valid input')
    sys.exit(1)

try:
    print(f'{X} / {Y} = {X/Y}')
except ZeroDivisionError:
    print('Cannot divide by 0')
    sys.exit(1)
