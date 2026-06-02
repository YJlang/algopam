# 햄버거 만들기
def solution(ingredient):
    answer = 0
    stack = []
    for i in ingredient:
        stack.append(i)
        print(stack[-4:])
        
        if stack[-4:] == [1, 2, 3, 1]:
            stack.pop()
            stack.pop()
            stack.pop()
            stack.pop()
            answer += 1
            
    return answer

print(solution([1, 3, 2, 1, 2, 1, 3, 1, 2])) 