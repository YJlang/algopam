#BOJ 20310: 타노스
#https://www.acmicpc.net/problem/20310

import sys

input = sys.stdin.readline

S = input()
zero = 0 #0의 개수
one = 0 #1의 개수
S_prime = ''

for i in S:
    if i == '0':
        zero += 1
    elif i == '1':
        one += 1

zero = zero // 2
one = one // 2


for j in range(0, zero):
    S_prime[j] += '0'

for k in range(0, one):
    S_prime[k] += '1'

print(S_prime)

