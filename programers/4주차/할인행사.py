#할인행사
from collections import Counter

def solution(want, number, discount):
    want_cnt = Counter(dict(zip(want, number)))
    answer = 0
    for i in range(len(discount) - 9):
        window = Counter(discount[i:i+10])
        if all(window[w] == c for w, c in want_cnt.items()):
            answer += 1
    return answer

print(solution(["banana", "apple", "rice", "pork", "pot"], 
                [3, 2, 2, 2, 1], 
                ["chicken", "apple", "apple", "banana", "rice",
                "apple", "pork", "banana", "pork", "rice", 
                "pot", "banana", "apple", "banana"]))
#정답: 3