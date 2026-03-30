import sys

input = sys.stdin.readline

n = int(input()) #조사한 시간
m = int(input()) #현재 터널 안의 차량 수
maximum = m #최대 차량 수
sj = []

for i in range(n):
    a, b = list(map(int, input().split())) #입구와 출구를 통과한 차량 수
    m += a - b
    if m < 0:
        maximum = 0
    if m > maximum:
        maximum = m
    sj.append(maximum)

dump = []
for j in sj:
    if j == 0:
        dump.append(0)
    else:
        dump.append(max(sj))

if 0 in dump:
    print(0)
else:
    print(max(dump))


