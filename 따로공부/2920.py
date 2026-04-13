#BOJ 2920: 음계
#https://www.acmicpc.net/problem/2920
#브론즈2

import sys

input = sys.stdin.readline

n = list(map(int, input().split())) #숫자 8개 입력받기

n_sort = sorted(n)
n_reverse_sort = sorted(n, reverse=True)

if n == n_sort:
    print("ascending")
elif n == n_reverse_sort:
    print("descending")
else:
    print("mixed") 