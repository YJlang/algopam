#서든어택3
#https://www.acmicpc.net/problem/22993

n = int(input())
arr = list(map(int,input().split()))

def sudden() :
    jun = arr.pop(0)
    arr.sort()

    for i in arr :
        if jun > i : 
            jun += i
        else :
            return "No"
    return "Yes"
print(sudden())