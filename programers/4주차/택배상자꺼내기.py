#택배상자꺼내기

# n = 택배 상자의 개수 13
# w = 가로로 놓는 상자의 개수 3
# num = 꺼내려는 택배 상자의 번호를 나타내는 정수 6
def solution(n, w, num):
    boxes = [] #최종적으로 박스가 담길 공간
    current = 1 # 담길 박스의 번호

    while current <= n:
        row = []
        # 상자 채우기
        for _ in range(w):
            if current <= n:
                row.append(current)
                current += 1
            else:
                # 상자가 없는 빈칸
                row.append(0) # 0은 빈칸을 의미
        
        # 홀수 번째 줄은 뒤집기
        if len(boxes) % 2 == 1:
            row.reverse()
        boxes.append(row)
    
    target_row = 0
    target_col = 0
    answer = 0

    for r in range(len(boxes)):
        for c in range(w):
            if boxes[r][c] == num:
                target_row = r
                target_col = c
    for r in range(target_row, len(boxes)):
        if boxes[r][target_col] != 0:
            answer += 1
        else:
            break

    
    return answer
    
print(solution(13, 3, 6))