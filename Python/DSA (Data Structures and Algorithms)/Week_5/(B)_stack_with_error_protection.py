import sys

stack = []

for command in sys.stdin:
    command = command.strip().split()

    if command[0] == "push":
        stack.append(int(command[1]))
        print("ok")

    elif command[0] == "pop":
        if stack:
            print(stack.pop())
        else:
            print("error")

    elif command[0] == "back":
        if stack:
            print(stack[-1])
        else:
            print("error")

    elif command[0] == "size":
        print(len(stack))

    elif command[0] == "clear":
        stack.clear()
        print("ok")

    elif command[0] == "exit":
        print("bye")
        break