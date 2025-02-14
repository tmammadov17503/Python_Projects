def smallest_sequence(N, K, A):
    stack = []

    for number in A:
        while K > 0 and stack and stack[-1] > number:
            stack.pop()
            K -= 1
        stack.append(number)

    while K > 0:
        stack.pop()
        K -= 1

    return stack

N, K = map(int, input().split()) #input handling
A = list(map(int, input().split()))

result = smallest_sequence(N, K, A)

print(" ".join(map(str, result)))