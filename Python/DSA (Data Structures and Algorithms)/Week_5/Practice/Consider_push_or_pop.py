import sys

def process_stack_operations(input_source):
    stack = []

    for command in input_source:
        command = command.strip().split()

        if not command:
            continue

        if command[0] == "push":
            stack.append(int(command[1]))

        elif command[0] == "pop":
            if stack:
                stack.pop()

    print(sum(stack))


if __name__ == "__main__":
    with open("input (1).txt", 'r') as file:
        process_stack_operations(file)