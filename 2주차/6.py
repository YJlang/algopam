#BOJ 7795: 먹을 것인가 먹힐 것인가
#https://www.acmicpc.net/problem/7795
import sys
from bisect import bisect_left #바이섹트, 이진탐색 라이브러리

input = sys.stdin.readline

t = int(input()) #테스트 케이스 개수

for _ in range(t):
    n, m = map(int, input().split()) #n은 a의 개수, m은 b의 개수
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    b.sort()
    
    result = 0
    for x in a:
        result += bisect_left(b, x) #x보다 작은 원소의 개수를 반환
    
    print(result)


    
