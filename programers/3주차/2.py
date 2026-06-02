# 카드 뭉치

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


print(solution(["i", "drink", "water"], ["i", "want", "to"], ["i", "want", "to", "drink", "water"]))