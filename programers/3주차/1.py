# 서울에서 김서방 찾기

def solution(seoul):
    answer = ''
    for i in seoul:
        if i == 'Kim':
            answer = f'김서방은 {seoul.index(i)}에 있다'    
            
            break
    return answer

print(solution(["Jane", "Kim"]))