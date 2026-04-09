#BOJ 1822: 차집합
#https://www.acmicpc.net/problem/1822
import sys

input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

a.sort()
b.sort()

result = []

for i in range(n):
    if a[i] not in b:
        result.append(a[i])

print(len(result))

for i in result:
    print(i, end=" ")