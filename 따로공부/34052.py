#백준 34052번 체육은 수학과목 입니다2
#https://www.acmicpc.net/problem/34052
#브론즈5
import sys

input = sys.stdin.readline
max = 1800
t = []
for _ in range(4):
    t.extend(list(map(int, input().split())))

correct = sum(t) + 300

if correct > max:
    print("No")
else:
    print("Yes")



    