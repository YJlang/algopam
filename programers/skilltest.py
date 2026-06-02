def solution(n):
    d = list(str(n))
    d.sort(reverse=True)
    answer = int("".join(d))
    return answer

print(solution(123145))