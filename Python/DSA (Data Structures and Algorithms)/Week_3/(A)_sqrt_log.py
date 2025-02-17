import math
import sys

max_num = 10**6
dp = [0] * (max_num + 1)
dp[0] = 1

for i in range(1, max_num + 1):
    val_1 = math.floor(i - math.sqrt(i))
    val_2 = math.floor(math.log(i)) if i > 1 else 0
    val_3 = math.floor(i * (math.sin(i) ** 2))
    dp[i] = (dp[val_1] + dp[val_2] + dp[val_3]) % 10**6

for line in sys.stdin:
    i = int(line.strip())
    if i == -1:
        break
    print(dp[i])