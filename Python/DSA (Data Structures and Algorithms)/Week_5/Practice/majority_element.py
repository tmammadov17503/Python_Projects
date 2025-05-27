# import sys
#
# def find_majority_element(filename):
#     try:
#         file = open(filename, 'r')
#         k = list(map(int, file.readline().split()))
#         file.close()
#     except FileNotFoundError:
#         print("Input file not found.")
#         return
#
#     n = len(k)
#     maj = None
#     cnt = 0
#
#     for num in k:
#         if cnt == 0:
#             maj = num
#             cnt = 1
#         elif num == maj:
#             cnt += 1
#         else:
#             cnt -= 1
#
#     if k.count(maj) > n // 2:
#         print(maj)
#     else:
#         print(-1)
#
# find_majority_element("majority.in.txt")


def find_majority_element_stack(arr):
    stack = []  # Stack to track potential majority element

    # Step 1: Finding the Candidate using Stack Operations
    for num in arr:
        if not stack:
            stack.append(num)  # Push if stack is empty
        elif stack[-1] == num:
            stack.append(num)  # Push if same as top element
        else:
            stack.pop()  # Pop if different element (simulate count decrease)

    # If stack is empty, no majority element exists
    if not stack:
        return -1

    # Step 2: Verify the Candidate
    candidate = stack[-1]  # The last element in stack is the potential majority
    count = sum(1 for x in arr if x == candidate)

    if count > len(arr) // 2:
        return candidate
    return -1  # No majority element

# Example usage
arr = list(map(int, input().split()))
print(find_majority_element_stack(arr))

