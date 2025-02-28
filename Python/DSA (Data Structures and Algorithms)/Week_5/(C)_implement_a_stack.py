import sys

stack = []
n = int(sys.stdin.readline().strip())

for i in range(n):
    operation = sys.stdin.readline().strip().split()

    if operation[0] == "1":
        stack.append(int(operation[1]))

    elif operation[0] == "2":
        print(stack.pop())
