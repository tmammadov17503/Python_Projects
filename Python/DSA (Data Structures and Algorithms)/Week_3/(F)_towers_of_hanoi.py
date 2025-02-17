def hanoi(n, from_peg, to_peg, aux_peg):
    if n == 0:
        return
    hanoi(n - 1, from_peg, aux_peg, to_peg)
    print(f"{from_peg} {to_peg}")
    hanoi(n - 1, aux_peg, to_peg, from_peg)

n = int(input().strip())

hanoi(n, 1, 2, 3)