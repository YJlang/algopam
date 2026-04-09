#BOJ 16916번: 부분 문자열
#https://www.acmicpc.net/problem/16916
import sys

input = sys.stdin.readline

S = input().strip() #풀네임
P = input().strip() #부분 문자열


#in 연산자로 부분 문자열 찾기
if P in S:
    print(1)
else:
    print(0) 