import sys
from collections import deque

def throwing_cards(n):
    if n == 0:
        return

    dq = deque(range(1, n + 1))
    discarded = []

    while len(dq) > 1:
        discarded.append(dq.popleft())
        dq.append(dq.popleft())

    print("Discarded cards:", ", ".join(map(str, discarded)) if discarded else "None")
    print("Remaining card:", dq[0])

for line in sys.stdin:
    n = int(line.strip())
    if n == 0:
        break
    throwing_cards(n)