#BOJ 1822: 차집합
#https://www.acmicpc.net/problem/1822
import sys

input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))

#set의 특징은 중복을 허용하지 않음
#x in set의 시간복잡도가 O(1)이다. 즉 엄청빠름
#순서가 보장되지 않음

#----#

#반면에 list는 왜느릴까...
#리스트는 원소가 줄줄이 한 칸씩 들어있는 구조임
#예를 들어 x in my_list를 하면 보통 앞에서부터 하나씩 비교함
#그러다 x를 찾으면 바로 반환하고, 끝까지 찾지 못하면 반환하지 않음
#즉, 최악의 경우 O(n)의 시간복잡도를 가짐

b = set(map(int, input().split())) #set은 내장함수가 아닌 집합 자료형을 만드는 도구


#시간복잡도 O(n log n + m)
a.sort() #n에 대한 정렬이므로 시간복잡도 O(n log n)
result = [i for i in a if i not in b] #b에 대한 탐색이므로 시간복잡도 O(m) 

print(len(result))
if result:
    print(*result)