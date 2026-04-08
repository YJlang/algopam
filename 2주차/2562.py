#2주차 과제 BOJ2562
#https://www.acmicpc.net/problem/2562

import sys
input = sys.stdin.readline

num = []
for i in range(9):
    n = int(input())
    if(i < 100):
        num.append(n)

print(max(num))
print(num.index(max(num)) + 1)
