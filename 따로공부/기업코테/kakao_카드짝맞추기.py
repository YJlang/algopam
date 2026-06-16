# 카드 짝 맞추기 (2021 KAKAO BLIND) - lesson 72415
# 핵심: "짝 맞추는 순서"를 완전탐색(DFS) + "두 점 사이 최소 키 횟수"를 BFS

from collections import deque, defaultdict


def solution(board, r, c):
    board = [row[:] for row in board]

    # 1) 카드 종류별 두 좌표 모으기  예: pos[1] = [(0,0),(3,2)]
    pos = defaultdict(list)
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                pos[board[i][j]].append((i, j))
    types = set(pos.keys())

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상하좌우

    # Ctrl+방향키: 그 방향 가장 가까운 카드로 점프, 없으면 벽 끝으로
    def ctrl_move(bd, sr, sc, dr, dc):
        nr, nc = sr, sc
        while True:
            tr, tc = nr + dr, nc + dc
            if not (0 <= tr < 4 and 0 <= tc < 4):  # 벽이면 멈춤
                break
            nr, nc = tr, tc
            if bd[nr][nc] != 0:                    # 카드 만나면 멈춤
                break
        return (nr, nc)

    # start -> end 까지 최소 키 횟수 (방향키4 + Ctrl방향키4, 모두 비용 1 -> BFS)
    def bfs(bd, start, end):
        if start == end:
            return 0
        visited = {start}
        q = deque([(start, 0)])
        while q:
            (cr, cc), d = q.popleft()
            for dr, dc in dirs:
                cands = []
                ar, ac = cr + dr, cc + dc            # 방향키 한 칸
                if 0 <= ar < 4 and 0 <= ac < 4:
                    cands.append((ar, ac))
                cands.append(ctrl_move(bd, cr, cc, dr, dc))  # Ctrl 점프
                for nx in cands:
                    if nx not in visited:
                        if nx == end:
                            return d + 1
                        visited.add(nx)
                        q.append((nx, d + 1))
        return 10 ** 9  # 4x4에선 도달 못 할 일 없음

    best = [float("inf")]

    # 2) 어떤 종류부터 맞출지 완전탐색 (남은 카드 상태를 들고 다니며)
    def dfs(bd, cur, remaining, cost):
        if cost >= best[0]:      # 가지치기: 이미 최선보다 크면 중단
            return
        if not remaining:        # 다 맞췄다
            best[0] = min(best[0], cost)
            return
        for t in remaining:
            a, b = pos[t]
            for first, second in ((a, b), (b, a)):   # 쌍 내부 순서 2가지
                # 카드1로 이동 + Enter, 카드2로 이동 + Enter  (두 번째 Enter에서 짝 제거)
                d1 = bfs(bd, cur, first) + 1
                d2 = bfs(bd, first, second) + 1
                nb = [row[:] for row in bd]          # 보드 복사 후 짝 제거
                nb[first[0]][first[1]] = 0
                nb[second[0]][second[1]] = 0
                dfs(nb, second, remaining - {t}, cost + d1 + d2)

    dfs(board, (r, c), types, 0)
    return best[0]


if __name__ == "__main__":
    print(solution([[1, 0, 0, 3], [2, 0, 0, 0], [0, 0, 0, 2], [3, 0, 1, 0]], 1, 0))  # 14
