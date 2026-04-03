# 백준 1009번 분산처리
# https://www.acmicpc.net/problem/1009
# 브론즈2
import sys

input = sys.stdin.readline

T = int(input())

for _ in range(T):
    a, b = map(int, input().split())
    last_digit = pow(a, b, 10)

    if last_digit == 0:
        print(10)
    else:
        print(last_digit)
