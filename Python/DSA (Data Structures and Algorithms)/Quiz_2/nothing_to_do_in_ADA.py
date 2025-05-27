# import sys
# from collections import deque
#
# dq = deque()
#
# with open("input.txt", "r") as file:
#     q = int(file.readline().strip())
#     commands = [line.strip().split() for line in file]
#
# sum_output = 0
#
# for command in commands:
#     if command[0] == "toFront":
#         dq.appendleft(int(command[1]))
#     elif command[0] == "push_back":
#         dq.append(int(command[1]))
#     elif command[0] == "front":
#         if dq:
#             num = dq.popleft()
#             print(num)
#             sum_output += num
#         else:
#             print("Nothing to do in ADA")
#     elif command[0] == "back":
#         if dq:
#             num = dq.pop()
#             print(num)
#             sum_output += num
#         else:
#             print("Nothing to do in ADA")
#     elif command[0] == "reverse":
#         dq.reverse()
#
# print(sum_output)

import sys
from collections import deque
with open("input (1).txt") as f:
    lines = f.read().splitlines()
dq = deque()
s = 0
try:
    q = int(lines[0])
    cmds = lines[1:q+1]
except ValueError:
    cmds = lines
for cmd in cmds:
    parts = cmd.split()
    if parts[0] == "toFront":
        dq.appendleft(int(parts[1]))
    elif parts[0] == "push_back":
        dq.append(int(parts[1]))
    elif parts[0] == "reverse":
        dq.reverse()
    elif parts[0] == "front":
        if dq:
            s += dq.popleft()
    elif parts[0] == "back":
        if dq:
            s += dq.pop()
print(s)