def compute_xnor(a, b):
    xor_result = a ^ b
    xnor_result = ~xor_result & 0xFFFFFFFF
    if xnor_result > 0x7FFFFFFF:
        xnor_result -= 0x100000000
    return xnor_result

def operation():
    n = int(input())
    arr = list(map(int, input().split()))
    q = int(input())

    prefix_xnor = [0] * (n + 1)

    for prefix in range(1, n + 1):
        prefix_xnor[prefix] = compute_xnor(prefix_xnor[prefix - 1], arr[prefix - 1])

    results = []
    for bit in range(q):
        l, r = map(int, input().split())
        result = compute_xnor(prefix_xnor[r], prefix_xnor[l - 1])
        results.append(result)

    print("\n".join(map(str, results)))

operation()