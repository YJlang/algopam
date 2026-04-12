#BOJ 2577: 숫자의 개수
#https://www.acmicpc.net/problem/2577
#브론즈2
import sys

input = sys.stdin.readline

a = int(input()) #시간복잡도 O(1)
b = int(input()) #시간복잡도 O(1)
c = int(input()) #시간복잡도 O(1)

result = a * b * c #시간복잡도 O(1)
result = str(result) #시간복잡도 O(n)

for i in range(10): #시간복잡도 O(10)
    print(result.count(str(i))) #count는 시간복잡도 O(n)