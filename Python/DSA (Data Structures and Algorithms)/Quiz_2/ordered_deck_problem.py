from collections import deque
n = int(input())
d = deque(range(n, 0, -1))
while len(d) > 1:
    d.popleft()
    d.append(d.popleft())
print(d[0])
