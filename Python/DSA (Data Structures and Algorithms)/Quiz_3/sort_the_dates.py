# n = int(input())
# dates = []
#
# for _ in range(n):
#     day, month, year = map(int, input().split('.'))
#     dates.append((year, month, day))
#
# dates.sort()
#
# for year, month, day in dates:
#     print(f"{day}.{month}.{year}")


# ONE VARIANT
# with open('input (1).txt', 'r') as file:
#     n = int(file.readline())
#     dates = []
#
#     # Read each date
#     for _ in range(n):
#         day, month, year = map(int, file.readline().split('.'))
#         dates.append((year, month, day))
#
# dates.sort()
#
# s345_date = dates[344]
#
# print(s345_date[2])

# WITH FILE HANDLING
file_path = 'input (1).txt'

with open(file_path, 'r') as file:
    n = int(file.readline())
    dates = [line.strip() for line in file.readlines()]

date_tuples = []
for date in dates:
    day, month, year = map(int, date.split('.'))
    date_tuples.append((year, month, day))

date_tuples.sort()

day_s345 = date_tuples[344][2]

print(day_s345)