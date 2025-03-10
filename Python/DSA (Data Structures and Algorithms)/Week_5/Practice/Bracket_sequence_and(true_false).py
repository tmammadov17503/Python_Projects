def is_valid_bracket_sequence(filename):
    try:
        file = open(filename, 'r')
        sequence = file.readline().strip()
        file.close()
    except FileNotFoundError:
        print("Input file not found.")
        return

    stack = []

    for char in sequence:
        if char == "(":
            stack.append(char)
        elif char == ")":
            if stack:
                stack.pop()
            else:
                print("false")
                return

    print("true" if not stack else "false")

is_valid_bracket_sequence("input (3).txt")