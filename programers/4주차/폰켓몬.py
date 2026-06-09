#폰켓몬

def solution(nums):
    # 최대 가질 수 있는 폰켓몬 수
    max_len = len(nums) // 2
    
    # 중복을 제거한 폰켓몬 수
    set_len = len(set(nums))

    return min(max_len, set_len)


print(solution([3,1,2,3]))