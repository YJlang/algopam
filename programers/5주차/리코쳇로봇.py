from collections import deque


def solution(board):
    n = len(board)        # 행(세로) 개수
    m = len(board[0])     # 열(가로) 개수

    # 1. 출발(R)과 목표(G) 좌표 찾기
    for i in range(n):
        for j in range(m):
            if board[i][j] == 'R':
                start = (i, j)
            elif board[i][j] == 'G':
                goal = (i, j)

    # 2. 방문 기록판
    visited = [[False] * m for _ in range(n)]

    # 3. 큐 초기화: (행, 열, 이동횟수)
    queue = deque()
    queue.append((start[0], start[1], 0))
    visited[start[0]][start[1]] = True

    # 4. 상 하 좌 우
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 5. BFS
    while queue:
        r, c, cnt = queue.popleft()

        if (r, c) == goal:          # 목표 도달 -> 최소 이동 횟수
            return cnt

        for dr, dc in directions:
            nr, nc = r, c
            # 벽이나 장애물에 부딪힐 때까지 미끄러짐
            while 0 <= nr + dr < n and 0 <= nc + dc < m and board[nr + dr][nc + dc] != 'D':
                nr += dr
                nc += dc

            if not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc, cnt + 1))

    # 6. 끝까지 못 만나면 도달 불가
    return -1
