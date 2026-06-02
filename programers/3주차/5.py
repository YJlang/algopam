# 마법의 엘리베이터

def solution(storey):
    answer = 0
    while storey > 0:
        digit = storey % 10
        if digit > 5:
            answer += 10 - digit
            storey += 10
        else:
            answer += digit
        storey //= 10
    return answer

print(solution(2554))    