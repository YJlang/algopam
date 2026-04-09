#1주차 과제 BOJ 1380: 귀걸이
#https://www.acmicpc.net/problem/1380
import sys

input = sys.stdin.readline

case = 1

name_correct = {}
while True:
    n = int(input())
    
    if n == 0:
        break

    names = [""] * (n + 1)
    count = [0] * (n + 1)

    # 이름
    for i in range(1, n + 1):
        names[i] = input()

    # 귀걸이 기록
    for _ in range(2 * n - 1):
        num, _ = input().split()
        count[int(num)] += 1

    # 한 번만 나온 학생 찾기
    for i in range(1, n + 1):
        if count[i] == 1:
            name_correct[case] = names[i]
            break
            

    case += 1

for i in range(1, case):
    print(i, name_correct[i])