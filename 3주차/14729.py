#BOJ 14729: 칠무해
#https://www.acmicpc.net/problem/14729

import sys

input = sys.stdin.readline

N = int(input())

list_num = []

if N >= 8 and N <= 10000000:
    for i in range(0, N):
        list_num.append(float(input()))

list_num.sort()

for i in range(0, 7):
    print(f"{list_num[i]:.3f}")