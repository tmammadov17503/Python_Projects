def is_valid_bracket_sequence(filename):
    try:
        file = open(filename, 'r')
        sequence = file.readline().strip()
        file.close()
    except FileNotFoundError:
        print("Input file not found.")
        return

    stack = []
    bracket_map = {')': '(', ']': '['}

    for char in sequence:
        if char in "([":
            stack.append(char)
        elif char in ")]":
            if stack and stack[-1] == bracket_map[char]:
                stack.pop()
            else:
                print("false")
                return

    print("true" if not stack else "false")


is_valid_bracket_sequence("input (4).txt")
