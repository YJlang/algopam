# 의상

def solution(clothes):
    answer = {}
    for cloth in clothes:
        answer[cloth[1]] = answer.get(cloth[1], 0) + 1
    ans = 1
    for value in answer.values():
        ans *= (value + 1)
    return ans - 1


print(solution([["yellow_hat", "headgear"], ["blue_sunglasses", "eyewear"], ["green_turban", "headgear"]]))
