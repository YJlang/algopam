#BOJ 2675: 문자열 반복
#https://www.acmicpc.net/problem/2675
#브론즈2
import sys

input = sys.stdin.readline

t = int(input()) #테스트 케이스 개수

for _ in range(t):
    r, s = input().split() #r은 반복 횟수, s는 문자열
    r = int(r) #시간복잡도 O(1)
    
    result = "" #시간복잡도 O(1)
    for char in s: #시간복잡도 O(n)
        result += char * r #시간복잡도 O(1)
    
    print(result) #시간복잡도 O(1)