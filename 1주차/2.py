import sys

input = sys.stdin.readline

c, k = map(int, input().split()) #c는 사탕 가격, k는 상근이가 갖고있는 지폐의 액면가에적힌 0의개수 k
sanggeun_money = 10 ** k #10의 k승 왜냐? 상근이는 10^k원짜리 지폐만 갖고있음

#예를 들어 c=184, k=1이면 sanggeun_money=10
#c + sanggeun_money // 2 --> 184 + 5 = 189
#189 // sanggeun_money --> 189 // 10 = 18
#18 * sanggeun_money --> 18 * 10 = 180
#응 테스트 다통과햇어 이거틀리면 자살함. 계산노가다까지함
print(((c + sanggeun_money // 2) // sanggeun_money) * sanggeun_money)
