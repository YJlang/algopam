#BOJ 2846: 오르막길
#https://www.acmicpc.net/problem/2846
import sys

input = sys.stdin.readline

n = int(input())
load = list(map(int, input().split())) #길

#오르막길의 최대 높이
best = 0
#오르막길의 시작점
start = load[0]

for i in range(1, n):
    if load[i] > load[i - 1]:
        best = max(best, load[i] - start)
    else:
        start = load[i]

print(best)
