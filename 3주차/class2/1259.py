#BOJ 1259: 팰린드롬수
#https://www.acmicpc.net/problem/1259
#브1

import sys
input = sys.stdin.readline

while True:
    n = input().strip()
    if n == "0":
        break
    if n == n[::-1]: #문자열 뒤집기 n[시작:끝:간격] -> 간격이 -1이면 뒤집기
        print("yes")
    else:
        print("no")