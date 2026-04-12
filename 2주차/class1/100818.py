#BOJ 100818: 최소, 최대
#https://www.acmicpc.net/problem/100818
#브론즈3
import sys

input = sys.stdin.readline

n = int(input())
num_list = list(map(int, input().split()))

print(min(num_list), max(num_list)) #min, max는 시간복잡도 O(n)