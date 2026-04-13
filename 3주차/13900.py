# BOJ 13900: 순서쌍의 곱의 합
# https://www.acmicpc.net/problem/13900

import sys

input = sys.stdin.readline

N = int(input())
numbers = list(map(int, input().split()))

list_sum = sum(numbers)
answer = 0

for number in numbers:
    list_sum -= number
    answer += number * list_sum

print(answer)
