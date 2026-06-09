def solution(participant, completion):
    answer = {}
    
    for name in participant:
        answer[name] = answer.get(name, 0) + 1
    print(answer)
    for name in completion:
        answer[name] -= 1
    print(answer)
    for name in answer:
        if answer[name] != 0:
            return name

print(solution(["leo", "kiki", "eden"], ["eden", "kiki"]))
