#1주차 과제 BOJ1440
#https://www.acmicpc.net/problem/1440
import sys

input = sys.stdin.readline

time = list(map(int, input().split(':')))

h,m,s = time[0],time[1],time[2]

cnt = 0

lists = [
    (h,m,s),
    (h,s,m),
    (m,h,s),
    (m,s,h),
    (s,h,m),
    (s,m,h)
]

for a, b, c in lists:
    if 1 <= a <= 12 and 0 <= b <= 59 and 0 <= c <= 59:
        cnt += 1

print(cnt)
