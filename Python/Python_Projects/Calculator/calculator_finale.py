import calc_logo
list_r = []
rest = 'y'

print(calc_logo.logo)
while rest.lower() == 'y':
    def calc(n1, n2, op):
        n1_1 = eval(n1)  # eval usage
        n2_2 = eval(n2)
        if op == "+":
            result = n1_1 + n2_2
        elif op == "-":
            result = n1_1 - n2_2
        elif op == "*":
            result = n1_1 * n2_2
        elif op == "/":
            result = n1_1 / n2_2
        else:
            print("Invalid operator")
            result = None
        expression = f"{n1} {op} {n2} = {result}"
        return result, expression

    if len(list_r) > 0:
        first_num = str(list_r[-1])  # last result as the first number
    else:
        first_num = input("What is the first number?\n")

    operator = input("+\n-\n*\n/\nWhat is the operator that you want to use?\n")
    second_num = input("What is the second number?\n")

    result, final_result = calc(first_num, second_num, operator)

    if result is not None:
        print(final_result)
        rest = input(f"Type 'y' to continue calculating with {result}, or type 'n' to stop:\n")
        list_r.append(result)

        if rest.lower() == 'n':
            rest = 'n'
        elif rest.lower() == 'y':
            rest = 'y'
            # print(list_r)
        else:
            print("Invalid input. Stopping calculation.")
            rest = 'n'
    else:
        rest = 'n'




# OTHER SOLUTION 
# from art import logo
#
# def add(n1, n2):
#   return n1 + n2
#
# def subtract(n1, n2):
#   return n1 - n2
#
# def multiply(n1, n2):
#   return n1 * n2
#
# def divide(n1, n2):
#   return n1 / n2
#
# operations = {
#   "+": add,
#   "-": subtract,
#   "*": multiply,
#   "/": divide
# }
#
# def calculator():
#   print(logo)
#
#   num1 = float(input("What's the first number?: "))
#   for symbol in operations:
#     print(symbol)
#   should_continue = True
#
#   while should_continue:
#     operation_symbol = input("Pick an operation: ")
#     num2 = float(input("What's the next number?: "))
#     calculation_function = operations[operation_symbol]
#     answer = calculation_function(num1, num2)
#     print(f"{num1} {operation_symbol} {num2} = {answer}")
#
#     if input(f"Type 'y' to continue calculating with {answer}, or type 'n' to start a new calculation: ") == 'y':
#       num1 = answer
#     else:
#       should_continue = False
#       clear()
#       calculator()
#
# calculator()
#