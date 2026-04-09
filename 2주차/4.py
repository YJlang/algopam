#BOJ 10826: 피보나치 수 4
#https://www.acmicpc.net/problem/10826
import sys

input = sys.stdin.readline

n = int(input())

fibo = [0] * (n + 1)

if n == 0:
    print(0)
elif n == 1:
    print(1)
else:
    fibo[1] = 1
    for i in range(2, n + 1):
        fibo[i] = fibo[i - 1] + fibo[i - 2]
    print(fibo[n])