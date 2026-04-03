#1942번: 디지털 시계
#https://www.acmicpc.net/problem/1942
import sys
input = sys.stdin.readline

for _ in range(3):
    start, end = input().split()

    h, m, s = map(int, start.split(":"))
    eh, em, es = map(int, end.split(":"))

    cnt = 0

    while True:
        # 시계 정수가 3의 배수인지 확인
        if (h * 10000 + m * 100 + s) % 3 == 0:
            cnt += 1

        # 종료 시각이면 멈춤
        if h == eh and m == em and s == es:
            break

        # 초를 1 올림
        s += 1

        # 60초가 되면? → 0초로 바꾸고, 분을 1 올림
        if s == 60:
            s = 0
            m += 1

        # 60분이 되면? → 0분으로 바꾸고, 시를 1 올림
        if m == 60:
            m = 0
            h += 1

        # 24시가 되면? → 0시로 바꿈 (자정 넘김!)
        if h == 24:
            h = 0

    print(cnt)
