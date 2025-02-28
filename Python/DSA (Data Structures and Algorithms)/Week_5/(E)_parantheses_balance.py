import sys

def is_balanced(sequence):
    stack = []
    bracket_map = {')': '(', ']': '['}

    for char in sequence:
        if char in "([":
            stack.append(char)
        elif char in ")]":
            if not stack or stack.pop() != bracket_map[char]:
                return "No"
    return "Yes" if not stack else "No"

n = int(sys.stdin.readline().strip())

for i in range(n):
    sequence = sys.stdin.readline().strip()
    print(is_balanced(sequence))