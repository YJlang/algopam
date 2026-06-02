# [Dreamhack misc] 폭탄 받아라! 풀이 회고 - 압축 폭탄 속 플래그 찾기

> 스포일러가 포함되어 있습니다. Dreamhack Wargame 2833번 `폭탄 받아라!`를 직접 풀고 싶은 분은 먼저 파일을 받아 관찰해 본 뒤 읽는 것을 추천합니다.

## 문제 정보

- 문제 링크: https://dreamhack.io/wargame/challenges/2833
- 플랫폼: Dreamhack
- 분야: misc
- 문제 번호: 2833
- 문제 제목: 폭탄 받아라!
- 분석 파일: `bomb`

문제 페이지는 로그인 후 자세히 볼 수 있어서, 이 글에서는 사용자가 받은 로컬 파일 `bomb`을 기준으로 분석했다. 처음에는 이름만 보고 CS:APP의 binary bomb 같은 실행 파일을 떠올렸는데, 실제로는 말 그대로 "폭탄"에 가까운 압축 파일이었다.

## 처음 관찰

파일 목록에서 확인한 `bomb`의 크기는 약 38KB였다.

```powershell
Get-Item .\bomb | Format-List Name,Length,FullName
```

결과:

```text
Name   : bomb
Length : 39196
```

크기가 작아서 실행 파일일 수도 있고, 압축 파일일 수도 있고, 단순 데이터일 수도 있다. 이럴 때 바로 실행하거나 무작정 압축 해제하기보다 먼저 앞부분의 바이트를 확인하는 것이 좋다.

```powershell
$bytes = [IO.File]::ReadAllBytes((Resolve-Path .\bomb))
($bytes[0..15] | ForEach-Object { $_.ToString('X2') }) -join ' '
```

결과:

```text
FD 37 7A 58 5A 00 00 04 E6 D6 B4 46 02 00 21 01
```

여기서 중요한 부분은 맨 앞의 `FD 37 7A 58 5A 00`이다. 이 값은 XZ 파일의 시그니처, 즉 "이 파일은 XZ 압축 파일입니다"라고 알려주는 매직 바이트다.

쉽게 말하면 파일 확장자가 없어도 파일 앞부분을 보면 정체를 추측할 수 있다. 이 문제의 `bomb`은 이름에는 확장자가 없지만 실제 내용은 XZ 압축 파일이었다.

## 왜 조심해야 할까?

이 파일은 압축 폭탄처럼 동작한다. 압축 파일 자체는 작지만, 압축을 풀면 훨씬 큰 데이터가 나온다.

이번 파일의 실제 크기는 다음과 같았다.

```text
압축 전 파일 크기: 39,196 bytes
압축 해제 후 크기: 268,349,468 bytes
압축 해제 비율: 약 6,846배
```

약 38KB짜리 파일이 압축을 풀면 약 256MiB가 된다. 이번 문제에서는 감당 가능한 크기였지만, 같은 방식으로 몇 GB나 몇 TB까지 커지는 파일도 만들 수 있다. 그래서 정체를 모르는 압축 파일은 함부로 더블클릭하거나 전체 해제하지 않는 편이 안전하다.

## 1차 풀이: 일단 풀어서 확인하기

처음에는 Python의 `lzma` 모듈로 압축을 풀어 임시 파일을 만들었다.

```python
import lzma
from pathlib import Path

src = Path("bomb")
dst = Path("tmp/bomb.unxz")

dst.write_bytes(lzma.decompress(src.read_bytes()))

print(dst.stat().st_size)
print(dst.read_bytes()[:16])
```

출력:

```text
268349468
b'0000000000000000'
```

압축을 풀어 보니 시작 부분은 전부 문자 `0`이었다. 중간과 끝부분도 샘플링해 봤는데 대부분 `0`이었다.

```python
from pathlib import Path

p = Path("tmp/bomb.unxz")
size = p.stat().st_size

for offset in [0, 1024, 1024 * 1024, size // 2, size - 1024]:
    with p.open("rb") as f:
        f.seek(offset)
        data = f.read(32)
    print(offset, data)
```

처음에는 "그냥 0만 잔뜩 있는 파일인가?" 싶었지만, 전체 바이트를 세어 보니 `0`이 아닌 값이 아주 조금 섞여 있었다.

```python
from pathlib import Path
from collections import Counter

p = Path("tmp/bomb.unxz")
counts = Counter()

with p.open("rb") as f:
    while True:
        chunk = f.read(1024 * 1024)
        if not chunk:
            break
        counts.update(chunk)

print("전체 크기:", p.stat().st_size)
print("서로 다른 바이트 개수:", len(counts))
print("가장 많이 나온 바이트:", counts.most_common(10))
```

결과:

```text
전체 크기: 268349468
서로 다른 바이트 개수: 20
가장 많이 나온 바이트: [(48, 268349440), ...]
```

여기서 `48`은 ASCII 코드로 문자 `'0'`이다. 전체 268,349,468바이트 중 268,349,440바이트가 `'0'`이었다. 즉 거의 전부가 `0`이고, 딱 28바이트만 다른 문자였다.

## 플래그 위치 찾기

`0`이 아닌 바이트가 있는 위치를 찾으면 플래그가 나올 가능성이 높다.

```python
from pathlib import Path

p = Path("tmp/bomb.unxz")
positions = []

with p.open("rb") as f:
    offset = 0

    while True:
        chunk = f.read(1024 * 1024)
        if not chunk:
            break

        for i, b in enumerate(chunk):
            if b != ord("0"):
                positions.append(offset + i)

        offset += len(chunk)

print("0이 아닌 바이트 개수:", len(positions))
print("첫 위치:", positions[0])
print("마지막 위치:", positions[-1])

start = max(0, positions[0] - 64)
end = positions[-1] + 64

with p.open("rb") as f:
    f.seek(start)
    context = f.read(end - start)

print(context)
```

결과:

```text
0이 아닌 바이트 개수: 28
첫 위치: 134131712
마지막 위치: 134131739

b'0000000000000000000000000000000000000000000000000000000000000000AF{BOOM_This_is_a_zip_bomb}\n000000000000000000000000000000000000000000000000000000000000000'
```

플래그:

```text
AF{BOOM_This_is_a_zip_bomb}
```

중간에 정말 작은 문자열 하나를 숨겨 두고, 앞뒤를 전부 `0`으로 채운 구조였다.

## 더 안전한 풀이: 압축 해제 파일을 만들지 않고 찾기

위 방식은 이해하기 쉽지만, 큰 압축 폭탄을 만나면 위험할 수 있다. 압축 해제 결과를 통째로 디스크에 저장하기 때문이다.

더 좋은 방법은 압축을 조금씩 풀면서 필요한 정보만 찾는 것이다. 아래 코드는 `bomb`을 작은 조각으로 읽고, `lzma.LZMADecompressor`로 스트리밍 해제하면서 `AF{...}` 패턴을 찾는다.

```python
import lzma
from pathlib import Path

src = Path("bomb")
decompressor = lzma.LZMADecompressor()

offset = 0
buffer = b""
flag = None

with src.open("rb") as f:
    while True:
        compressed_chunk = f.read(4096)
        if not compressed_chunk:
            break

        # 압축 데이터를 조금씩 해제한다.
        chunk = decompressor.decompress(compressed_chunk)

        # 플래그가 chunk 경계에 걸칠 수 있어서 이전 끝부분을 조금 붙여 둔다.
        data = buffer + chunk

        start = data.find(b"AF{")
        if start != -1:
            end = data.find(b"}", start)
            if end != -1:
                flag = data[start : end + 1].decode()
                break

        # 다음 chunk와 이어 볼 수 있도록 마지막 일부만 보관한다.
        buffer = data[-100:]
        offset += len(chunk)

print(flag)
```

출력:

```text
AF{BOOM_This_is_a_zip_bomb}
```

이 방식의 장점은 압축 해제 결과 전체를 파일로 만들지 않는다는 점이다. 이번 문제처럼 결과가 256MiB 정도면 괜찮지만, 진짜 악성 압축 폭탄이라면 디스크나 메모리를 크게 잡아먹을 수 있다.

## 사용한 개념 정리

### 매직 바이트

매직 바이트는 파일 맨 앞에 붙는 고유한 바이트 패턴이다. 운영체제나 분석 도구는 이 값을 보고 파일 형식을 추측한다.

예를 들어 이번 파일은 다음 값으로 시작했다.

```text
FD 37 7A 58 5A 00
```

이 값은 XZ 압축 파일의 시그니처다. 그래서 확장자가 없어도 "이건 XZ 압축 파일이구나"라고 판단할 수 있었다.

### XZ와 lzma

XZ는 압축 파일 형식이고, Python의 `lzma` 모듈은 XZ/LZMA 압축을 다룰 수 있게 해 주는 표준 라이브러리다.

```python
import lzma

data = lzma.decompress(compressed_data)
```

이 코드는 압축된 바이트를 받아 원래 바이트로 되돌린다. 다만 `decompress()`를 한 번에 쓰면 압축 해제 결과 전체가 메모리에 올라올 수 있다. 그래서 큰 파일이 의심될 때는 `LZMADecompressor`처럼 조금씩 처리하는 방식을 쓰는 편이 더 안전하다.

### 압축 폭탄

압축 폭탄은 작은 압축 파일이지만, 압축을 풀면 매우 큰 데이터가 생성되는 파일을 말한다. 보안 문제에서는 "무작정 압축 해제하면 위험하다"는 습관을 묻는 장치로 자주 쓰인다.

이번 문제의 구조는 단순했다.

```text
엄청 많은 '0'
+ 중간의 플래그 문자열
+ 다시 엄청 많은 '0'
```

반복되는 문자는 압축이 매우 잘 된다. 그래서 원본은 256MiB 정도인데 압축 파일은 38KB 정도까지 줄어든 것이다.

## 시간 복잡도

여기서 `n`을 압축 해제 후 데이터의 크기라고 하자. 이 문제에서는 `n = 268,349,468`바이트다.

처음 방식처럼 압축을 전부 풀고 전체를 훑으면 시간 복잡도는 `O(n)`이다. 압축 해제 결과의 모든 바이트를 한 번씩 확인하기 때문이다. 입력 크기가 두 배가 되면 확인해야 할 바이트 수도 거의 두 배가 된다.

공간 복잡도는 방식에 따라 다르다.

- 압축 해제 결과를 파일로 저장하는 방식: 디스크 공간 `O(n)`이 필요하다.
- `lzma.decompress()`로 한 번에 메모리에 올리는 방식: 메모리 `O(n)`이 필요할 수 있다.
- 스트리밍으로 조금씩 확인하는 방식: 작은 버퍼만 유지하므로 추가 메모리는 거의 `O(1)`에 가깝다.

이 문제에서는 시간 자체보다 공간 사용이 더 중요했다. 압축 폭탄 문제의 핵심은 "얼마나 빨리 푸느냐"보다 "풀다가 내 환경을 터뜨리지 않느냐"에 가깝다.

## 풀이하면서 헷갈렸던 점

처음에는 파일 이름이 `bomb`이라서 실행 파일을 분석해야 하는 리버싱 문제처럼 느껴졌다. 그런데 문자열을 뽑아 보니 의미 있는 실행 파일 문자열이 나오지 않았고, 앞부분 매직 바이트를 확인하니 XZ 압축 파일이었다.

또 하나 재밌었던 점은 압축 해제 결과의 시작과 끝만 보면 전부 `0`이라서 플래그가 없는 것처럼 보인다는 점이다. 이때 샘플링만 하고 끝내면 놓칠 수 있다. 전체에서 `0`이 아닌 바이트의 위치를 세어 보니 중간에 딱 플래그가 숨어 있었다.

## 최종 정리

이번 문제에서 배운 점은 세 가지다.

1. 확장자가 없어도 매직 바이트를 보면 파일 형식을 추측할 수 있다.
2. 압축 파일은 바로 풀기 전에 크기와 형식을 먼저 의심해야 한다.
3. 큰 파일을 다룰 때는 전체를 메모리나 디스크에 올리는 방식보다 스트리밍 분석이 더 안전하다.

풀이 자체는 짧았지만, misc 문제답게 "도구를 얼마나 많이 아느냐"보다 "파일을 어떻게 조심스럽게 관찰하느냐"를 묻는 문제였다. 다음부터 수상한 파일을 만나면 일단 실행이 아니라 관찰부터 해야겠다.

## 참고

- Dreamhack Wargame 2833: https://dreamhack.io/wargame/challenges/2833
- Python `lzma` 공식 문서: https://docs.python.org/3/library/lzma.html
- XZ Utils 파일 형식 문서: https://tukaani.org/xz/xz-file-format.txt
