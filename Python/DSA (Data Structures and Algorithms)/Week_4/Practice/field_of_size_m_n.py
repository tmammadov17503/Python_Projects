import math
m, n = map(int, input().split())
R = m if m % 2 == 1 else m - 1
up_moves = (R - 1) // 2
right_moves = n - 1
total_moves = up_moves + right_moves
print(math.comb(total_moves, up_moves))
