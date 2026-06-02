def solution(arr):
    answer = [0, 0] # answer[0] = 0의 개수, answer[1] = 1의 개수
    def compress(x, y, size):
        first = arr[x][y]
        
        #현재 영역이 모두 같은 값인지?
        for i in range(x, x + size):
            for j in range(y, y + size):
                if arr[i][j] != first:
                    #같은 값이 아니라면 4개로 분할
                    half = size // 2
                    compress(x, y, half)
                    compress(x + half, y, half)
                    compress(x, y + half, half)
                    compress(x + half, y + half, half)
                    return
        
        #현재 영역이 모두 같은 값이면 answer에 추가
        answer[first] += 1

    compress(0, 0, len(arr))
    return answer

arr = [
    [1,1,0,0],
    [1,0,0,0],
    [1,0,0,1],
    [1,1,1,1]
]

print(solution(arr)) # 출력: [4, 9]