# 백준 4999번 아!
# https://www.acmicpc.net/problem/4999
# 브론즈5
import sys

input = sys.stdin.readline

jh = input().strip()
doctor = input().strip()

jh_a = 0
jh_h = 0
doctor_a = 0
doctor_h = 0

for j in jh:
    if j == "a":
        jh_a += 1
    elif j == "h":
        jh_h += 1

for d in doctor:
    if d == "a":
        doctor_a += 1
    elif d == "h":
        doctor_h += 1

if jh_a >= doctor_a and jh_h >= doctor_h:
    print("go")
else:
    print("no") 