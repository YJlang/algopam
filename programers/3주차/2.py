# 카드 뭉치
"""오답
def solution(cards1, cards2, goal):
    answer = ''
    c1 = len(cards1)
    c2 = len(cards2)

    for i in reversed(goal):
        if c1 > 0 and cards1[c1-1] == i:
            c1 -= 1
        elif c2 > 0 and cards2[c2-1] == i:
            c2 -= 1
        else:
            answer = 'No'
            break

    if answer == '':
        answer = 'Yes'  

    return answer


print(solution(["i", "drink", "water"], ["i", "want", "to"], ["i", "want", "to", "drink", "water"]))"""

# # 정답 코드
# def solution(cards1, cards2, goal):
#     i = 0 # cards1에서 현재 확인할 위치
#     j = 0 # cards2에서 현재 확인할 위치

#     for word in goal:
#         if i < len(cards1) and cards1[i] == word:
#             i += 1
#         elif j < len(cards2) and cards2[j] == word:
#             j += 1
#         else:
#             return "No"
#     return "Yes"

from collections import deque

def solution(cards1, cards2, goal):
    c1 = deque(cards1)
    c2 = deque(cards2)

    for word in goal:
        if c1 and c1[0] == word:
            c1.popleft()
        elif c2 and c2[0] == word:
            c2.popleft()
        else:
            return "No"
    return "Yes"

print(solution(["i", "drink", "water"], ["want", "to"], ["i", "want", "to", "drink", "water"]))