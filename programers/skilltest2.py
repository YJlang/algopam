#점심시간에 도둑이 들었음.
# 체육복이 있는 학생이 이들에게 체육복을 빌려주려고 함.
# 체격순서고, 바로 앞번호의 학생이나 바로 뒷번호의 학생에게만 체육복을 빌려줄 수 있음.a
# 예를 들어, 4번 학생은 3번 학생이나 5번 학생에게만 체육복을 빌려줄 수 있음. 
#체육복이 없으면 수업을 들을 수 없기 때문에 체육복을 적절히 빌려 최대한 많은 학생이 체육쉅을 들어야 함

n = 0 # 전체 학생의 수 2명 이상 30명 이하
lost = [] # 도난당한 학생들의 번호가 담긴 배열
reverse = [] # 여벌 체육복을 가진 학생들의 번호가 담긴 배열

def solution(n, lost, reverse):
    answer = n - len(lost)
    for i in lost:
        if i in reverse:
            answer += 1
            reverse.remove(i)
        elif i - 1 in reverse:
            answer += 1
            reverse.remove(i - 1)
        elif i + 1 in reverse:
            answer += 1
            reverse.remove(i + 1)
    return answer

print(solution(5, [2, 4], [1, 3, 5])) # 출력: 4