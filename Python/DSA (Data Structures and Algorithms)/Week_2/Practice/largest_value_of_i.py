def func(a, b):
    i = 0
    while a % (b ** (i + 1)) == 0:
        i += 1
    return i

a, b = map(int, input().split())
print(func(a, b))




# #include<stdio.h>
# #include<cstring>
#
# int f(int a, int b)
# {
# 	if (a % b != 0)
# 		return 0;
# 	if (a % b == 0)
# 		return f(a / b,b) + 1;
# }
# int main() {
# 	int a, b;
# 	scanf_s("%d %d", &a, &b);
# 	printf("%d", f(a, b));
# }