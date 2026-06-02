# MTaquitous 분석 진행사항

작성 시점: 2026-04-27

## 문제 개요

- 대회: 2026 GM 해커톤
- 문제: 1번
- 목표: 취약점을 찾아 공격하여 서버의 `flag` 파일 읽기
- 원격 서버:
  - `nc host8.dreamhack.games 21640`
  - `http://host8.dreamhack.games:21640/`

## 로컬 파일 구조

```text
MTaquitous/
├─ Dockerfile
├─ flag
└─ deploy/
   ├─ prob
   └─ prog.bin
```

- `Dockerfile`
  - Ubuntu 24.04 기반
  - `pwn` 유저로 `/home/pwn/prob` 실행
  - `socat TCP-LISTEN:8080,reuseaddr,fork EXEC:./prob,stderr`
  - `flag` 권한은 `644`
- `flag`
  - 로컬 더미 플래그: `DH{flag}`
- `deploy/prob`
  - 64-bit Linux ELF
  - C++ 기반 VM 인터프리터
  - PIE 바이너리
  - VM 내부에 MTE 비슷한 태그 검사가 구현되어 있음
- `deploy/prog.bin`
  - `prob`가 읽어서 실행하는 VM 바이트코드
  - 실제 note 메뉴 로직은 이 파일에 들어 있음

## 원격 메뉴

접속하면 다음 메뉴가 출력된다.

```text
1) add note
2) link note
3) edit note
4) show note
5) delete note
6) exit
>
```

## 전체 구조

`prob`는 note 기능을 네이티브 코드로 직접 구현한 프로그램이 아니라, 자체 VM을 초기화한 뒤 `prog.bin`을 VM 바이트코드로 실행한다.

확인한 VM syscall 번호:

```text
0: read
1: write
2: mmap
3: munmap
```

`prob` 문자열에서 확인한 VM 관련 panic 메시지:

```text
[CPU PANIC]
[MTE PANIC]
[RAM PANIC]
Invalid VA: PGD/PUD/PMD entry not present
MTE tag mismatch at address ...
Safe write out of bounds
Safe read out of bounds
Unknown SYSCALL number
HALT instruction executed
```

## note 구조

`prog.bin`을 40바이트 VM instruction 단위로 디코딩해서 본 결과, note는 대략 다음 구조로 보인다.

```c
note_table[index] = note_ptr;

note_ptr + 0x00 : linked note pointer
note_ptr + 0x08 : size
note_ptr + 0x10 : user data
```

즉 각 note는 `0x10` 바이트짜리 헤더 뒤에 사용자 데이터가 붙는 구조다.

## 기능별 동작 요약

### add note

대략적인 흐름:

```text
Index? 입력
Size? 입력
mmap(size + 0x10)
note[0x00] = 0
note[0x08] = size
Data? 입력
read data -> note + 0x10
note_table[index] = note
```

관찰 결과:

- `size <= 0xfff0` 정도는 정상 처리된다.
- `size >= 0xfff1`부터는 `note + 0x10 + size`가 다음 VM page로 넘어가며 MTE panic이 자주 발생한다.
- `size = 0x10000`도 add 중 MTE panic이 발생한다.
- `size = 0xffffffffffffffff` 같은 값은 산술 wrap 때문에 add/delete 흐름이 이상하게 정상처럼 보일 수 있지만, 이 경우 큰 delete 검증으로 바로 해석하면 안 된다. 실제 data 입력과 size 처리 동기화가 꼬이기 쉽다.

### link note

대략적인 흐름:

```text
Index? A
Index? B
note_A와 note_B가 존재하면:
    *(note_A + 0x00) = note_B
```

즉 note 안의 linked pointer를 설정한다.

### edit note

대략적인 흐름:

```text
Index? 입력
note가 없으면 메뉴로 복귀
Data? 입력
note + 0x10에 note->size만큼 복사

linked pointer를 따라가며:
    linked_note + 0x10에도 같은 길이만큼 복사
```

중요한 점:

- linked note에 쓸 때 linked note 자신의 size를 다시 확인하지 않는다.
- 따라서 큰 note를 작은 note에 link하면 작은 note의 data 영역에서 overflow가 가능하다.
- 다만 write 시작 지점은 항상 `linked_note + 0x10`이므로, linked note의 헤더 자체를 바로 덮는 primitive는 아니다.

### show note

대략적인 흐름:

```text
Index? 입력
note가 없으면 "No note"
write(1, note + 0x10, note->size)
```

### delete note

대략적인 흐름:

```text
Index? 입력
note가 없으면 메뉴로 복귀
munmap(note, note->size + 0x10)
note_table[index] = 0
```

중요한 점:

- note table의 해당 entry만 0으로 만든다.
- 다른 note가 linked pointer로 가리키고 있던 값은 정리하지 않는다.
- 따라서 dangling linked pointer가 남는다.

## 확인한 취약점

### 1. linked edit size confusion

`edit`은 linked note에 복사할 때 linked note 자신의 size를 보지 않고, 원본 note의 size를 기준으로 복사한다.

예시:

```text
add note0, size = big
add note1, size = small
link note0 -> note1
edit note0
```

원격에서 확인한 현상:

```text
note1 before: BBBBBBBB
edit note0:   CCCCCCCC
show note1:   CCCCCCCC
```

### 2. delete 후 dangling link

`delete`는 note table entry만 지우고 linked pointer는 정리하지 않는다.

예시:

```text
add note0
add note1
link note0 -> note1
delete note1
edit note0
```

원격에서 확인한 MTE panic:

```text
[MTE PANIC] MTE tag mismatch at address 0xa3ba010:
pointer tag = 0x8, memory tag = 0xe
```

### 3. UAF 태그 brute force 가능성

삭제된 note와 같은 VA/tag 조합이 재사용되면 dangling linked pointer를 통해 새 note를 건드릴 수 있다.

실험 흐름:

```text
add note0
add note1
link note0 -> note1
delete note1
add note2
edit note0
show note2
```

32회 시도 중 1회 정도 `note2`가 `edit note0`의 영향을 받는 것을 확인했다.

```text
success 1 / 32
show note2 -> DDDDDDD
```

즉 MTE는 완전한 방어라기보다는 확률 방어에 가깝다.

### 4. signed index bypass / OOB index

index 검사가 `index < 16`만 확인하고, `index >= 0`을 확인하지 않는다.

`18446744073709551615`는 unsigned 입력으로는 큰 값이지만 signed 관점에서는 `-1`처럼 동작한다. 그래서 검사 통과 후 note table 기준 `-8` 위치에 접근하려다 MTE panic이 난다.

원격 재현:

```text
[MTE PANIC] MTE tag mismatch at address 0x2f02ff8:
pointer tag = 0x7, memory tag = 0x0
```

또한 `2^63 + offset/8` 형태의 index를 쓰면 signed 비교는 통과하면서 실제 주소 계산은 note table 뒤쪽 offset을 가리킬 수 있다.

짧은 OOB scan 결과:

- `offset 0x00`: note0 entry라 정상적으로 `MARK0000` 출력
- `offset 0x08`부터 `0x300` 근처까지 대부분 `No note`
- `+0x2e0` 근처에서 처음에는 애매한 출력이 있었지만 재확인 결과 단순 동기화 문제였고 `No note`로 판단

즉 note table이 있는 VM page 안의 가까운 뒤쪽 qword들은 대부분 0으로 보인다.

추가로 `add`에서도 OOB index가 그대로 적용되는 것을 확인했다.

```text
offset 0x80  add/show 성공
offset 0x88  add/show 성공
offset 0x100 add/show 성공
offset 0x300 add/show 성공
offset 0x800 add/show 성공
offset 0xf00 add/show 성공
offset 0xff8 add/show 성공
offset 0x1000부터는 MTE panic
```

해석:

- 원래 note table은 16개 entry, 즉 `0x80` 바이트만 의도한 것으로 보인다.
- 하지만 실제로는 같은 VM page 안의 qword slot을 `0xff8`까지 note slot처럼 쓸 수 있다.
- page 경계를 넘는 `0x1000`부터는 MTE tag가 맞지 않아 panic이 난다.
- 이 덕분에 최대 512개 정도의 note pointer slot을 만들 수 있어, heap/VM page grooming과 UAF brute force에는 도움이 된다.
- 다만 지금까지는 이 범위 안에 바로 덮을 수 있는 중요 VM 변수는 보이지 않았다. 같은 page가 note table 전용/여유 공간처럼 쓰이는 듯하다.

## VM mmap/munmap 구현 분석

`prob`의 syscall dispatcher에서 `0xfe` opcode가 VM syscall을 수행한다.

주요 함수:

```text
0x2f20: physical page allocator
0x3780: freed physical page를 free-list/tree에 삽입
0x3b60: random VA allocator
0x3e60: random MTE tag 생성
0x4210: MTE tag check
0x74de: syscall 2 mmap case 진입
0x72fc: syscall 3 munmap case 진입
```

추가로 확인한 VM memory access 특징:

```text
0x4e60: VM store helper 계열
0x5a10: VM load helper 계열
```

이 load/store helper들은 상위 page-table entry가 존재하는지는 확인하지만, leaf PTE의 present bit를 엄격하게 확인하지 않는 흐름으로 보인다. PTE 값에서 physical frame 부분만 mask해서 VM RAM base에 더한다.

이 점 때문에 `munmap` 후 leaf PTE의 present bit가 내려가도, MTE tag만 맞으면 stale VA로 freed physical page에 접근할 수 있다. 원격에서 관찰한 UAF hit가 이 동작과 잘 맞는다.

### syscall 2: mmap

대략적인 동작:

```text
addr = syscall_arg_addr
length = syscall_arg_length
tag = random_nibble()

for each 0x1000 page in range(addr, addr + length):
    if 필요한 page-table level이 없으면:
        0x2f20 allocator로 page-table page 할당

    data_page = 0x2f20 allocator로 physical page 할당
    PTE = data_page | present_bit | tag_bits

해당 VA 범위의 MTE tag storage를 tag로 채움
return tagged_va = (tag << 60) | addr
```

중요한 점:

- `mmap`은 data page뿐 아니라 필요한 page-table page도 `0x2f20` allocator로 만든다.
- PTE에는 physical page base, present bit, tag 관련 bit가 같이 들어간다.
- 반환 포인터는 상위 4비트에 MTE tag가 붙은 tagged pointer다.

### 0x2f20 physical page allocator

`0x2f20`은 VM RAM 안의 0x1000 단위 physical page를 할당한다.

대략적인 동작:

```text
if free-list/tree가 비어 있지 않으면:
    free-list에서 page frame 하나를 꺼냄
    allocation bitmap에 used bit 설정
    return frame << 12

else:
    allocation bitmap을 선형 탐색해서 빈 page frame을 찾음
    used bit 설정
    return frame << 12
```

따라서 `munmap`으로 반환된 data page는 이후 `mmap`에서 data page나 page-table page로 재사용될 수 있다.

### syscall 3: munmap

대략적인 동작:

```text
addr = syscall_arg_addr
length = syscall_arg_length
tag = random_nibble()

for each 0x1000 page in range(addr, addr + length):
    MTE tag check(addr + offset)
    page table walk
    leaf PTE에서 physical frame 추출

    allocation bitmap에서 해당 physical frame의 used bit clear
    free-list/tree에 physical frame 삽입
    leaf PTE present bit clear
    해당 VA page의 MTE tag storage를 새 random tag로 덮음

return 0
```

중요한 점:

- `munmap`은 leaf PTE의 present bit를 clear한다.
- data physical page는 free-list로 돌아간다.
- 비어 있는 상위 page-table page를 회수하는 코드는 현재까지 보이지 않는다.
- leaf PTE 값 자체는 0으로 지우지 않는다. 따라서 MTE tag만 맞으면 stale VA가 아직 같은 physical frame을 계산할 수 있다.

추가 xref 확인:

```text
0x741a call 0x3780   # munmap 루프 안의 free-list 삽입
0x757e call 0x2f20   # mmap data page 할당
0x75ea call 0x2f20   # mmap page-table level 할당
0x7617 call 0x2f20   # mmap page-table level 할당
0x7634 call 0x2f20   # mmap page-table level 할당
```

`0x3780` 호출은 현재 확인 범위에서 `munmap` 루프 안 한 곳만 보인다.

## “큰 size delete로 page table UAF 가능?” 현재 판단

현재까지는 **직접적인 page-table UAF 가능성은 낮다**고 본다.

이유:

```text
munmap은 leaf PTE를 찾아 data physical page만 free-list에 넣는다.
그 후 leaf PTE present bit를 clear한다.
상위 page-table page를 비우거나 free-list에 넣는 코드는 보이지 않는다.
```

따라서 `delete(note)`에서 `note->size`를 크게 만들더라도, 그 효과는 “넓은 VM VA 범위의 data page들을 munmap”하는 쪽에 가깝다. page-table page 자체가 곧바로 UAF 상태가 되는 루트는 아직 확인되지 않았다.

다만 간접 가능성은 남아 있다.

```text
1. 큰 size delete로 여러 data page를 free-list에 넣음
2. 이후 mmap/add가 그 physical page를 page-table page로 재사용
3. 기존 dangling pointer가 같은 physical page를 여전히 접근할 수 있다면 page table 조작 가능
```

하지만 이 시나리오는 약점이 있다.

```text
munmap 시 기존 VA의 PTE present bit가 clear된다.
기존 VA로 다시 접근하면 보통 Invalid VA 또는 MTE panic이 난다.
같은 VA/tag 조합으로 재매핑되거나, 다른 dangling 경로가 있어야 한다.
```

즉 지금 우선순위는 “page table UAF”보다는 다음 방향이 더 현실적이다.

```text
1. data page UAF + MTE tag brute force를 안정화
2. linked edit size confusion으로 같은 page 안에서 쓸 수 있는 범위 확인
3. OOB index로 note table page 주변의 유효 포인터 후보 탐색
4. note metadata를 조작할 수 있는 2차 primitive 확보
5. show/edit/delete primitive를 임의 VM memory read/write로 확장
```

## 원격 실험 메모

### size별 add/delete 반응

짧게 확인한 값:

```text
size 0x0       add/delete 정상
size 0x1       add/delete 정상
size 0x8       add/delete 정상
size 0xff0     add/delete 정상
size 0xff8     add/delete 정상
size 0xfff     add/delete 정상
size 0x1000    add/delete 정상
size 0xfff0    add/delete 정상
size 0xfff1    add 중 MTE panic
size 0x10000   add 중 MTE panic
```

`0xfff1` 이상에서 add가 먼저 죽기 때문에, 단순히 add에서 큰 size note를 만든 뒤 delete로 page table UAF를 만드는 방향은 막힌다.

큰 delete를 시도하려면 결국 `note->size`를 나중에 조작해야 한다. 현재 확인한 linked edit overflow는 linked note의 data 영역부터 쓰므로, note header의 size를 바로 바꾸지는 못한다.

또한 size를 조작해 실제 매핑보다 더 넓은 범위를 `munmap`하게 만들더라도, 첫 번째 unmapped page나 tag가 맞지 않는 page에서 MTE panic이 날 가능성이 높다. 이 경우 이미 앞쪽 page들이 partial unmap될 수는 있지만, 프로세스가 죽으면 같은 세션에서 exploit을 이어가기 어렵다. 따라서 큰 delete를 exploit으로 쓰려면 “panic 없이 통과하는 연속 VA/tag 범위”를 먼저 만들어야 한다.

## 현재 결론

현재까지 확인한 가장 강한 primitive는 다음 세 가지다.

```text
1. linked pointer dangling UAF
2. linked edit size confusion
3. signed index bypass를 통한 note table page OOB 접근
4. OOB add로 note slot을 16개 제한보다 훨씬 많이 확보
```

반면, “큰 size delete로 page table UAF를 직접 만든다”는 가설은 현재 구현 분석과 원격 반응 기준으로는 약하다.

다음 단계는 page-table UAF에 계속 매달리기보다, data-page UAF를 안정화해서 note 포인터나 size를 조작할 수 있는 경로를 찾는 것이 좋아 보인다.

## 최종 exploit 후보: VA overlap + tag match

`mmap`의 random VA는 대략 다음 형태다.

```text
random_8bytes & 0xffff000
```

즉 0x1000 단위로 정렬된 256MB 근처의 VM VA 공간에서 랜덤 주소를 고른다. note는 작은 size를 넣어도 내부적으로 최소 `0x10000` 정도의 mapping을 잡는다.

중요한 관찰:

```text
새 mmap이 이미 매핑된 VA page를 고르면 기존 PTE를 overwrite한다.
이때 기존 physical page를 free하지는 않는다.
해당 VA의 MTE tag storage는 새 tag로 바뀐다.
```

따라서 두 note mapping이 VA 범위에서 겹치고, 새 tag가 예전 pointer tag와 우연히 같으면, 예전 note table entry가 죽지 않고 새 mapping 안의 데이터를 note header처럼 해석할 수 있다.

예를 들어 새 note가 `B`에 잡히고 예전 note가 `B + 0x1000`에 있었다면:

```text
old note header      = B + 0x1000
new note data offset = 0xff0 부근부터 old header를 제어 가능
```

새 note payload에 다음 구조를 0x1000마다 심어두면 overlap/tag match를 감지할 수 있다.

```text
B + d + 0x00: fake link = 0
B + d + 0x08: fake size = 8
B + d + 0x10: marker = "OV...."
```

그 뒤 `show(old)`가 원래 old note 내용이 아니라 marker를 출력하면, old note entry가 새 note payload 안의 fake header를 보고 있다는 뜻이다.

이 상태에서 `link old, current`를 호출하면 VM이 실제 `current note pointer`를 fake header의 link 위치에 써준다. 그 위치는 current note의 data 영역 안이므로 `show(current)`로 raw pointer를 leak할 수 있다.

자동화 스크립트:

```text
MTaquitous/exploit_probe.py
```

사용 예:

```bash
python MTaquitous/exploit_probe.py --host host8.dreamhack.games --port 21640 --notes 512
```

현재 원격 포트가 `ConnectionRefused` 상태라 실제 최종 hit까지는 이어서 검증하지 못했다. 포트가 다시 열리면 이 스크립트로 overlap/tag hit를 먼저 잡고, leak된 note pointer를 이용해 table control 또는 fake note primitive로 확장하는 것이 다음 작업이다.

## double-free 가능성 메모

`munmap`은 leaf PTE의 present bit만 내리고 PTE 값을 완전히 지우지 않는다. 또한 load/store helper도 leaf present bit를 엄격하게 보지 않는 것으로 보인다.

그래서 이론적으로는 다음 흐름이 가능해 보인다.

```text
1. note A delete
2. A의 VA page tag가 새 random tag로 바뀜
3. 같은 VA에 새 tag를 맞춘 stale/fake pointer로 다시 접근
4. 같은 PTE의 physical frame을 다시 munmap
5. 같은 frame이 free-list에 중복 삽입되는 double-free 가능
```

문제는 두 번째 접근에 필요한 MTE tag를 알아야 한다는 점이다. tag는 4비트라 brute force 대상이지만, 틀리면 panic으로 세션이 죽는다. 따라서 이 루트는 table control이나 pointer leak 이후에 시도하는 것이 현실적이다.
