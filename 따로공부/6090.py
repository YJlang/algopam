import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    out = []

    for _ in range(t):
        n = data[pos]
        pos += 1

        xs = [0] * n
        ys = [0] * n
        for i in range(n):
            xs[i] = data[pos]
            ys[i] = data[pos + 1]
            pos += 2

        # edge i = v[i] -> v[i+1]
        ex = [0] * n
        ey = [0] * n
        for i in range(n - 1):
            ex[i] = xs[i + 1] - xs[i]
            ey[i] = ys[i + 1] - ys[i]
        ex[-1] = xs[0] - xs[-1]
        ey[-1] = ys[0] - ys[-1]

        corners = []
        for i in range(n):
            if ex[i - 1] * ey[i] - ey[i - 1] * ex[i] != 0:
                corners.append(i)

        m = len(corners)
        prev_corner = [0] * n
        next_corner = [0] * n

        # Fill the nearest corner in each direction for every vertex.
        for idx, c in enumerate(corners):
            nxt = corners[(idx + 1) % m]
            cur = c
            while cur != nxt:
                next_corner[cur] = nxt
                cur += 1
                if cur == n:
                    cur = 0

        for idx, c in enumerate(corners):
            prv = corners[idx - 1]
            cur = c
            while cur != prv:
                prev_corner[cur] = prv
                cur -= 1
                if cur < 0:
                    cur = n - 1

        ans1 = 0

        # Case 1: pairs lying on one flat side between adjacent corners.
        for idx, c in enumerate(corners):
            d = corners[(idx + 1) % m]
            if (
                ex[c] * ey[d - 1] - ey[c] * ex[d - 1] <= 0
                and ex[d] * ey[c - 1] - ey[d] * ex[c - 1] <= 0
            ):
                cnt = (d - c) % n + 1
                ans1 += cnt * (cnt - 1) // 2

        ans2 = 0

        # Case 2: all other pairs. For each fixed i, the valid j-range is contiguous.
        for i in range(n):
            left = (next_corner[i] - i) % n + 1
            right = (prev_corner[i] - i) % n - 1
            if left > right:
                continue

            im1 = i - 1
            ex_im1 = ex[im1]
            ey_im1 = ey[im1]

            # First j such that the j -> i side becomes removable.
            lo, hi = left, right + 1
            while lo < hi:
                mid = (lo + hi) // 2
                j = i + mid
                if j >= n:
                    j -= n
                if ex[j] * ey_im1 - ey[j] * ex_im1 <= 0:
                    hi = mid
                else:
                    lo = mid + 1
            first_true = lo

            ex_i = ex[i]
            ey_i = ey[i]

            # Last j such that the i -> j side is still removable.
            lo, hi = left - 1, right
            while lo < hi:
                mid = (lo + hi + 1) // 2
                jm1 = i + mid - 1
                if jm1 >= n:
                    jm1 -= n
                if ex_i * ey[jm1] - ey_i * ex[jm1] <= 0:
                    lo = mid
                else:
                    hi = mid - 1

            if first_true <= lo:
                ans2 += lo - first_true + 1

        out.append(str(ans1 + ans2 // 2))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
