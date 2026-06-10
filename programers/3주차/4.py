# 멀리 뛰기

# def solution(n):
#     if n == 1:
#         return 1
#     if n == 2:
#         return 2
    
#     a, b = 1, 2
#     for i in range(2, n):
#         a, b = b, (a+b)%1234567 # 동시대입법
#     return b

# print(solution(4))

def solution(n):
    if n <= 2:
        return n
    
    dp = [0] * (n+1)
    dp[1] = 1
    dp[2] = 2

    for i in range(3, n+1):
        dp[i] = (dp[i-1] + dp[i-2]) % 1234567
    
    return dp[n]

print(solution(4))