# BOJ 20310: 타노스
# https://www.acmicpc.net/problem/20310

import sys
input = sys.stdin.readline

S = input().strip()

remove_zero = S.count('0') // 2
remove_one = S.count('1') // 2

removed = [False] * len(S)

# 1은 앞에서부터 지워야 앞쪽의 큰 문자를 없앨 수 있다
cnt = 0
for i in range(len(S)):
    if S[i] == '1' and cnt < remove_one:
        removed[i] = True
        cnt += 1

# 0은 뒤에서부터 지워야 앞쪽의 작은 문자를 최대한 남길 수 있다
cnt = 0
for i in range(len(S) - 1, -1, -1):
    if S[i] == '0' and cnt < remove_zero:
        removed[i] = True
        cnt += 1

print(''.join(S[i] for i in range(len(S)) if not removed[i]))
