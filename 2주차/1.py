#2주차 과제 BOJ 15953: 상금 헌터
#https://www.acmicpc.net/problem/15953
import sys

input = sys.stdin.readline

t = int(input())

a_prize_list = [5000000, 3000000, 2000000, 500000, 300000, 100000] 
b_prize_list = [5120000, 2560000, 1280000, 640000, 320000] 

for i in range(t):
    a, b = map(int, input().split())
    a_prize = 0
    b_prize = 0
    if a == 1:
        a_prize = a_prize_list[0]
    elif 1 < a <= 3:
        a_prize = a_prize_list[1]
    elif 3 < a <= 6:
        a_prize = a_prize_list[2]
    elif 6 < a <= 10:
        a_prize = a_prize_list[3]
    elif 10 < a <= 15:
        a_prize = a_prize_list[4]
    elif 15 < a <= 21:
        a_prize = a_prize_list[5]
    
    if b == 1:
        b_prize = b_prize_list[0]
    elif 1 < b <= 3:
        b_prize = b_prize_list[1]
    elif 3 < b <= 7:
        b_prize = b_prize_list[2]
    elif 7 < b <= 15:
        b_prize = b_prize_list[3]
    elif 15 < b <= 31:
        b_prize = b_prize_list[4]
    
    print(a_prize + b_prize)

    
    