def evaluate_rpn_expression(filename):
    try:
        file = open(filename, 'r')
        expression = file.readline().strip()
        file.close()
    except FileNotFoundError:
        print("Input file not found.")
        return

    stack = []
    tokens = expression.split()

    for token in tokens:
        if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()

            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a // b)

    print(stack[0])

evaluate_rpn_expression("input (2).txt")