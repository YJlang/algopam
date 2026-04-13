#BOJ 2435: 기상청 인턴 신현수
#https://www.acmicpc.net/problem/2435
#브론즈1

import sys

input = sys.stdin.readline

N, K = map(int, input().split())

list_num = list(map(int, input().split()))

list_sum = []

for i in range(0, N-K+1):
    list_sum.append(sum(list_num[i:i+K]))

print(max(list_sum))