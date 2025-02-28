import sys
from collections import deque

dq = deque()

for command in sys.stdin:
    command = command.strip().split()

    if command[0] == "push_front":
        dq.appendleft(int(command[1]))
        print("ok")

    elif command[0] == "push_back":
        dq.append(int(command[1]))
        print("ok")

    elif command[0] == "pop_front":
        if dq:
            print(dq.popleft())
        else:
            print("error")

    elif command[0] == "pop_back":
        if dq:
            print(dq.pop())
        else:
            print("error")

    elif command[0] == "front":
        if dq:
            print(dq[0])
        else:
            print("error")

    elif command[0] == "back":
        if dq:
            print(dq[-1])
        else:
            print("error")

    elif command[0] == "size":
        print(len(dq))

    elif command[0] == "clear":
        dq.clear()
        print("ok")

    elif command[0] == "exit":
        print("bye")
        break