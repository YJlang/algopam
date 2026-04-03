# 백준 28444번 HI-ARC=?
# https://www.acmicpc.net/problem/28444
# 브론즈5
import sys

input = sys.stdin.readline

H, I, A, R, C = map(int, input().split())

result = (H * I) - (A * R * C)

print(result)