import sys

stack = []
sequence = sys.stdin.readline().strip()

for char in sequence:
    if char == "(":
        stack.append(char)
    elif char == ")":
        if stack:
            stack.pop()
        else:
            print("NO")
            exit()

print("YES" if not stack else "NO")
