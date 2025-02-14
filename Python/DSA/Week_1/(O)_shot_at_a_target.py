# def func(n, m, a, b):
#     # we have n shots and magazine with m cartriges
#     # full load for some seconds or 1 cartrige for b sec
#     # 1 shot n takes 1 second
#
#     seconds = 0
#     seconds += a  # first load
#     shots_needed = n
#     shots = 0
#     if n > m:
#         for shoot in range(m + 1):
#             shots += 1
#             if shots == m and n - m == 1:
#                 seconds += b
#             elif (n-m)>=m:
#                 seconds += a
#
#             if shots == shots_needed:
#                 seconds += shots_needed
#                 break
#         return seconds
#
#
# n, m, a, b = map(int, input().split())
# print(func(n, m, a, b))

def func(n, m, a, b):
    shots_fired = 0
    time_taken = 0

    while shots_fired < n:
        bullets_to_load = min(m, n - shots_fired)
        time_taken += min(a, bullets_to_load * b)
        time_taken += bullets_to_load
        shots_fired += bullets_to_load

    return time_taken

n, m, a, b = map(int, input().split())
print(func(n, m, a, b))