#2주차 과제 BOJ11720
#https://www.acmicpc.net/problem/11720

import sys
input = sys.stdin.readline

n = int(input())
number = list(input().strip())

sum = 0

for i in number:
    sum += int(i)

print(sum)

