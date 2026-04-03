#삼각형 만들기 2622
import sys
input = sys.stdin.readline

N = int(input())
cnt = 0

for i in range(1, N+1):
    for ii in range(i, N+1):
        iii = N - (i+ii)
        
        if iii >= i + ii:
            continue
        else:
            if ii > iii:
                break
            cnt += 1

print(cnt)