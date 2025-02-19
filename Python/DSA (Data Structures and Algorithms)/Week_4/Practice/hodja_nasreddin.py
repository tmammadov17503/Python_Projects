MOD = 1234

def compute_binomials(max_n, mod):
    binom = [[0] * (max_n + 1) for _ in range(max_n + 1)]
    for i in range(max_n + 1):
        binom[i][0] = 1
        binom[i][i] = 1
        for j in range(1, i):
            binom[i][j] = (binom[i-1][j-1] + binom[i-1][j]) % mod
    return binom

n, m = map(int, input().split())
max_val = n + m
binom = compute_binomials(max_val, MOD)

total = 0
for i in range(1, n + 1):
    for j in range(1, m + 1):
        ways_hodja = binom[i + j - 2][i - 1]
        ways_donkey = binom[(n - i) + (m - j)][n - i]
        total = (total + ways_hodja * ways_donkey) % MOD

print(total)