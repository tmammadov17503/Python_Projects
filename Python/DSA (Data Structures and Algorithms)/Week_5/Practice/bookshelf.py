from collections import deque


def simulate_book_shelf(filename):
    try:
        file = open(filename, 'r')
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        print("Input file not found.")
        return

    n = int(lines[0].strip())
    dq = deque()
    sum_removed_left = 0

    for i in range(1, n + 1):
        command = list(map(int, lines[i].strip().split()))

        if command[0] == 1:
            dq.appendleft(command[1])
        elif command[0] == 2:
            dq.append(command[1])
        elif command[0] == 3:
            if dq:
                sum_removed_left += dq.popleft()
        elif command[0] == 4:
            if dq:
                dq.pop()

    print(sum_removed_left)

simulate_book_shelf("input.txt")