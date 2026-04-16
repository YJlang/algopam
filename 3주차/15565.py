#BOJ 15565: 귀여운 라이언
#https://www.acmicpc.net/problem/15565\

import sys
input = sys.stdin.readline

n, k = map(int, input().split())
dolls = list(map(int, input().split()))

left = 0
ryan_count = 0 #현재 구간 안의 라이언(1) 개수
result = float('inf') #결과값 초기화(무한대)

for right in range(n):
    #right 포인터가 라이언이면 카운트 증가
    if dolls[right] == 1:
        ryan_count += 1

    #라이언이 k개 이상이면 -> 구간 줄이기 시도
    while ryan_count >= k:
        result = min(result, right - left + 1)

        if dolls[left] == 1:
            ryan_count -= 1
        left += 1
print(result if result != float('inf') else -1)







#BOJ 15565: 귀여운 라이언
#https://www.acmicpc.net/problem/15565\

import sys
input = sys.stdin.readline

n, k = map(int, input().split())
dolls = list(map(int, input().split()))

left = 0
ryan_count = 0 #현재 구간 안의 라이언(1) 개수
result = float('inf') #결과값 초기화(무한대)

for right in range(n):
    #right 포인터가 라이언이면 카운트 증가
    if dolls[right] == 1:
        ryan_count += 1

    #라이언이 k개 이상이면 -> 구간 줄이기 시도
    while ryan_count >= k:
        result = min(result, right - left + 1)

        if dolls[left] == 1:
            ryan_count -= 1
        left += 1
print(result if result != float('inf') else -1)


#제공해주신 소스 코드 내용을 살펴보면, 아쉽게도 현재 텍스트에는 `for`문 내부의 `while`문 코드가 잘려 있어서 직접적으로 확인되지 않습니다. 

#하지만 백준 15565번 '귀여운 라이언' 문제를 풀기 위해 사용하는 '투 포인터(Two Pointers)' 알고리즘의 구조를 생각해보면, 질문하신 `while`문이 어떤 역할을 하는지 쉽게 유추할 수 있습니다. 저의 프로그래밍 배경지식을 바탕으로 이전 답변의 '손가락 비유'를 연장해서 설명해 드릴게요. **(※ 참고: 아래 설명하는 `while`문의 구체적인 동작 원리는 제공된 소스 텍스트 외의 정보입니다.)**

#이전 답변에서 `for`문은 **오른쪽 손가락(`right`)을 한 칸씩 이동시키며 라이언을 줍는 과정**이라고 말씀드렸습니다. 여기에 `while`문과 왼쪽 손가락(`left`)이 추가되면 두 손가락이 다음과 같이 협동하게 됩니다.

#**1. `while`문은 언제 켜질까?**
#* 오른쪽 손가락(`right`)을 계속 이동하며 라이언을 줍다가, 마침내 우리가 목표로 한 **라이언 인형 K개를 모두 다 찾았을 때** 비로소 `while`문이 작동하기 시작합니다. (코드로는 `while ryan_count == k:` 처럼 작성됩니다.)

#**2. `while`문 안에서는 무슨 일을 할까? (길이 줄이기 작전)**
#* 라이언 K개를 모았으니, 이제 **"이 인형 무더기의 길이를 최대한 짧게 좁혀보는 작업"**을 합니다.
#* **길이 재기:** 우선 지금 두 손가락 사이의 길이를 재서, 지금까지 찾은 길이 중 가장 짧다면 결과값(`result`)에 기록해 둡니다.
#* **왼쪽 손가락 이동:** 뻗어두었던 **왼쪽 손가락(`left`)을 오른쪽으로 한 칸 좁힙니다**. 즉, 맨 왼쪽에 있던 인형 하나를 우리 구역에서 과감하게 버리는 것입니다.
#* **라이언 개수 차감:** 만약 방금 버린 인형이 '라이언'이었다면? 안타깝게도 우리 구역 안에 있는 라이언 개수(`ryan_count`)에서 1을 빼야 합니다.

#**3. `while`문이 진짜 어려운 이유: 왜 반복할까?**
#`while`문이 어려운 이유는 조건이 맞으면 계속 반복되기 때문입니다. 
#* 왼쪽 손가락을 좁혀서 맨 왼쪽 인형을 하나 버렸는데, **만약 그 인형이 라이언이 아니라 다른 인형(어피치)이었다면?** 우리 구역 안에는 여전히 라이언이 K개 남아있을 것입니다.
#* 그러면 `while`문은 멈추지 않고 **"오, 아직도 라이언이 K개네? 조건 만족! 그럼 길이를 더 줄일 수 있으니 왼쪽 손가락을 한 칸 더 좁혀보자!"**라며 다시 반복됩니다.
#* 이렇게 맨 왼쪽 인형을 버리다가, 마침내 **'라이언 인형'을 버리게 되어 구역 내 라이언이 K개 미만으로 줄어들면** 그제서야 `while`문을 빠져나옵니다. 그리고 다시 `for`문으로 돌아가 오른쪽 손가락(`right`)을 움직여 새로운 라이언을 찾으러 갑니다.

#**💡 핵심 요약**
#* **`for`문 (오른쪽 손가락):** "라이언이 K개가 될 때까지 구역을 넓히자!"
#* **`while`문 (왼쪽 손가락):** "라이언 K개를 채웠으니, 더 이상 뺄 인형이 없을 때까지 구역을 최대한 좁혀보자!"

#이 두 손가락이 애벌레처럼 늘어났다 줄어들었다를 반복하며 가장 짧은 길이를 찾아내는 것이 핵심입니다. 이해가 안 가는 부분이 있다면 편하게 다시 질문해 주세요! 혹시 잘려나간 `while`문 코드가 있다면 마저 붙여넣어 주시면 더 정확하게 설명해 드리겠습니다.
