#boj14582
#https://www.acmicpc.net/problem/14582
import sys

input = sys.stdin.readline

#제미니스 점수 1회초~9회초
jm = list(map(int, input().split()))
#걸리버스 점수 1회말~9회말
gl = list(map(int, input().split()))

jm_score = 0
gl_score = 0

for i in range(9):
    jm_score += jm[i]
    
    if jm_score > gl_score:
        print("Yes")
        break
    
    gl_score += gl[i]

if jm_score < gl_score:
    print("No")