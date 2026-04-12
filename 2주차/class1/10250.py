#BOJ 10250: ACM 호텔
#https://www.acmicpc.net/problem/10250
#브론즈2
import sys

input = sys.stdin.readline

t = int(input()) #테스트 케이스 개수

for _ in range(t):
    h, w, n = map(int, input().split()) #h는 층수, w는 호수, n은 손님 수
    
    if n % h == 0:
        print(h * 100 + n // h) #시간복잡도 O(1)
    else:
        print(n % h * 100 + n // h + 1) #시간복잡도 O(1)