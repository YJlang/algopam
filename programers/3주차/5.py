# 마법의 엘리베이터

# def solution(storey):
#     answer = 0
#     while storey > 0:
#         digit = storey % 10
#         if digit > 5:
#             answer += 10 - digit
#             storey += 10
#         else:
#             answer += digit
#         storey //= 10
#     return answer

# print(solution(2554))

def solution(storey):
    answer = 0
    while storey > 0:
        d = storey % 10 # 맨 끝자리 숫자

        if d < 5: # 작으면 --> 깎아서 0으로
            answer += d
            storey //= 10 # 끝자리 버리고 윗자리로 넘어감
        elif d > 5: # 크면 --> 올려서 윗자리로 올림
            answer += 10 - d
            storey = storey // 10 + 1
        else: # d == 5
            if (storey // 10) % 10 >= 5: # 윗자리도 크면 올리는 게 이득
                answer += 5
                storey = storey // 10 + 1
            else: # 아니면 그냥 깎기
                answer += 5
                storey //= 10
    return answer

print(solution(555))