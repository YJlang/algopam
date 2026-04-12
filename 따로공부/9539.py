import sys
import heapq


def solve():
    input = sys.stdin.buffer.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, target = map(int, input().split())
        target -= 1

        gain = list(map(int, input().split()))
        graph = [[] for _ in range(n)]
        for _ in range(n - 1):
            a, b = map(int, input().split())
            a -= 1
            b -= 1
            graph[a].append(b)
            graph[b].append(a)

        # Build the rooted tree at chamber 1.
        parent = [-1] * n
        order = [0]
        parent[0] = 0
        for u in order:
            for v in graph[u]:
                if parent[v] == -1:
                    parent[v] = u
                    order.append(v)

        # Mark the unique path 1 -> target.
        on_path = [False] * n
        path = []
        cur = target
        while True:
            path.append(cur)
            on_path[cur] = True
            if cur == 0:
                break
            cur = parent[cur]
        path.reverse()

        # heap_info[u] stores profitable "side quests" inside u's subtree.
        # Each pair (c, h) means:
        #   if current HP >= c before entering this subtree,
        #   then we can come back with HP increased by h (> 0).
        heap_info = [None] * n
        heap_size = [0] * n

        for u in reversed(order):
            if on_path[u]:
                continue

            big = []
            big_size = 0

            # Merge child heaps using small-to-large.
            for v in graph[u]:
                if parent[v] != u or on_path[v]:
                    continue
                child_heap = heap_info[v]
                child_size = heap_size[v]

                if child_size > big_size:
                    big, child_heap = child_heap, big
                    big_size, child_size = child_size, big_size

                if child_heap:
                    for item in child_heap:
                        heapq.heappush(big, item)
                    big_size += child_size

            # Entering chamber u itself.
            cur_c = -gain[u] if gain[u] < 0 else 0
            cur_h = gain[u]

            # If current segment is not yet profitable, or its requirement
            # is not smaller than the next quest's requirement, merge them.
            while big and (cur_h <= 0 or cur_c >= big[0][0]):
                nxt_c, nxt_h = heapq.heappop(big)
                big_size -= 1
                need = nxt_c - cur_h
                if need > cur_c:
                    cur_c = need
                cur_h += nxt_h

            if cur_h > 0:
                heapq.heappush(big, (cur_c, cur_h))
                big_size += 1

            heap_info[u] = big
            heap_size[u] = big_size

        hp = gain[0]
        if hp < 0:
            out.append("trapped")
            continue

        available = []

        def add_side_quests(path_node):
            for nxt in graph[path_node]:
                if on_path[nxt]:
                    continue
                if parent[nxt] == path_node and heap_info[nxt]:
                    for item in heap_info[nxt]:
                        heapq.heappush(available, item)

        def consume_all_possible():
            nonlocal hp
            while available and available[0][0] <= hp:
                hp += heapq.heappop(available)[1]

        add_side_quests(0)
        consume_all_possible()

        escaped = True
        for idx in range(1, len(path)):
            hp += gain[path[idx]]
            if hp < 0:
                escaped = False
                break

            add_side_quests(path[idx])
            consume_all_possible()

        out.append("escaped" if escaped else "trapped")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
