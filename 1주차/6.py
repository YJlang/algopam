import sys

input = sys.stdin.readline

n = int(input())
snow = list(map(int, input().split()))

time = 0

while True:
    snow.sort(reverse=True)

    if snow[0] == 0:
        print(time)
        break

    snow[0] -= 1

    if n > 1 and snow[1] > 0:
        snow[1] -= 1

    time += 1

    if time > 1440:
        print(-1)
        break
