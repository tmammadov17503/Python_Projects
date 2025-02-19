def solve():
    n = input().strip()

    prime_digits = {2, 3, 5, 7}
    total = 0

    for ch in n:
        d = int(ch)
        if d in prime_digits:
            total += d
        else:
            total += 1

    print(total)


if __name__ == "__main__":
    solve()
