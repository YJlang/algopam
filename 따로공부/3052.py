#BOJ 3052: 나머지
#https://www.acmicpc.net/problem/3052
#브론즈2

import sys

input = sys.stdin.readline

num_list = []

for _ in range(0, 10): #시간복잡도 O(1)
    n = int(input())
    if n <= 1000 and n > 0:
        num_list.append(n % 42)

print(len(set(num_list))) #set은 중복제거해줌
