s = "ABCDEFG"

# 기본: s[시작:끝]  →  시작 인덱스부터 끝 인덱스 '직전'까지
print(s[0:3])    # ABC       (인덱스 0,1,2)
print(s[2:5])    # CDE       (인덱스 2,3,4)
print(s[3:])     # DEFG      (3부터 끝까지)
print(s[:4])     # ABCD      (처음부터 3까지)

print("---")

# 간격 지정: s[시작:끝:간격]
print(s[::1])    # ABCDEFG   (1칸씩 앞으로, 기본값)
print(s[::2])    # ACEG      (2칸씩 건너뜀)
print(s[1::2])   # BDF       (인덱스 1부터 2칸씩)

print("---")

# 음수 간격: 뒤에서부터
print(s[::-1])   # GFEDCBA   (1칸씩 뒤로 = 뒤집기)
print(s[::-2])   # GECA      (2칸씩 뒤로)
print(s[4:1:-1]) # EDC       (인덱스 4에서 2까지 뒤로)

print("---")

# 음수 인덱스: 뒤에서부터 세기
print(s[-1])     # G         (맨 마지막)
print(s[-3:])    # EFG       (뒤에서 3개)
print(s[:-2])    # ABCDE     (맨 뒤 2개 제외)
print(s[-3:-1])  # EF        (뒤에서 3번째부터 마지막 직전까지)
