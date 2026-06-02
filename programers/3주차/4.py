# 멀리 뛰기

# def solution(n):
#     dp = [1, 2]
#     if n == 1:
#         return 1
#     if n == 2:
#         return 2

#     for i in range(2, n):
#         dp.append((dp[i-1] + dp[i-2]))
    
#     return dp[n-1]%1234567
    
# print(solution(4))

def solution(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    a, b = 1, 2
    for i in range(2, n):
        a, b = b, (a+b)%1234567
    return b

print(solution(3))  