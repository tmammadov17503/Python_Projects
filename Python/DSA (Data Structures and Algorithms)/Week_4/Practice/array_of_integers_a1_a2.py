arr = list(map(int, input().split()))
s = 0
res = 0
for x in arr:
    s += x
    res += s*s
print(res%67890)


# FOR INPUT FILES

# with open("input.txt", "r") as file:
#     arr = list(map(int, file.readline().split()))
#
# s = 0
# res = 0
# for x in arr:
#     s += x
#     res += s * s
#
# print(res % 67890)
