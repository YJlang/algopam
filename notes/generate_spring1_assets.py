from PIL import Image, ImageDraw, ImageFont
import math
import os


OUT_DIR = r"c:\algopam\notes\spring1-web-basics-assets"
FONT_REG = r"C:\Windows\Fonts\malgun.ttf"
FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def rounded(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, start, end, fill, width=10, head=18):
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=fill, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    left = (
        x2 - head * math.cos(angle) + head * 0.55 * math.sin(angle),
        y2 - head * math.sin(angle) - head * 0.55 * math.cos(angle),
    )
    right = (
        x2 - head * math.cos(angle) - head * 0.55 * math.sin(angle),
        y2 - head * math.sin(angle) + head * 0.55 * math.cos(angle),
    )
    draw.polygon([end, left, right], fill=fill)


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, box, font_obj, fill, line_gap=8):
    x1, y1, x2, _ = box
    width = x2 - x1
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for ch in paragraph:
            test = current + ch
            text_width = draw.textbbox((0, 0), test, font=font_obj)[2]
            if text_width <= width or not current:
                current = test
            else:
                lines.append(current)
                current = ch
        if current:
            lines.append(current)

    y = y1
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_obj)
        height = bbox[3] - bbox[1]
        draw.text((x1, y), line, font=font_obj, fill=fill)
        y += height + line_gap
    return y


def chip(draw: ImageDraw.ImageDraw, xy, label: str, fill, text_fill="white"):
    x, y = xy
    bbox = draw.textbbox((0, 0), label, font=font(24, bold=True))
    width = bbox[2] - bbox[0] + 34
    height = bbox[3] - bbox[1] + 20
    rounded(draw, (x, y, x + width, y + height), 18, fill)
    draw.text((x + 17, y + 8), label, font=font(24, bold=True), fill=text_fill)
    return width, height


def card(draw: ImageDraw.ImageDraw, box, title: str, subtitle: str, fill, accent, icon_text: str):
    rounded(draw, box, 28, fill, outline=accent, width=3)
    x1, y1, x2, y2 = box
    draw.ellipse((x1 + 22, y1 + 22, x1 + 98, y1 + 98), fill=accent)
    icon_font = font(44, bold=True)
    bbox = draw.textbbox((0, 0), icon_text, font=icon_font)
    draw.text(
        (x1 + 60 - (bbox[2] - bbox[0]) / 2, y1 + 60 - (bbox[3] - bbox[1]) / 2 - 4),
        icon_text,
        font=icon_font,
        fill="white",
    )
    draw.text((x1 + 106, y1 + 30), title, font=font(26, bold=True), fill="#1f2937")
    draw_wrapped(draw, subtitle, (x1 + 30, y1 + 118, x2 - 30, y2 - 30), font(24), "#374151", line_gap=6)


def create_restaurant_flow():
    img = Image.new("RGB", (1600, 920), "#fffaf2")
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((40, 40, 1560, 880), radius=36, fill="#fffdf8", outline="#f3e6cc", width=3)

    draw.text((90, 80), "웹 개발을 식당으로 보면 훨씬 쉽다", font=font(56, bold=True), fill="#111827")
    draw.text(
        (92, 158),
        "백엔드 개발자는 손님 앞에 서는 사람이 아니라, 뒤에서 주문을 처리하는 주방 팀에 가깝다.",
        font=font(28),
        fill="#6b7280",
    )

    boxes = [
        (
            (90, 250, 420, 560),
            "손님 = 클라이언트",
            "브라우저나 앱에서\n\"이 메뉴 주세요\"라고 요청을 보낸다.",
            "#fff7ed",
            "#f97316",
            "C",
        ),
        (
            (460, 250, 790, 560),
            "메뉴판 = API",
            "무엇을 주문할 수 있는지\n미리 약속해 둔 목록이다.",
            "#eff6ff",
            "#2563eb",
            "A",
        ),
        (
            (830, 250, 1160, 560),
            "주방 = Spring Boot",
            "요청을 받고, 규칙대로\n비즈니스 로직을 처리한다.",
            "#ecfdf5",
            "#10b981",
            "S",
        ),
        (
            (1200, 250, 1510, 560),
            "냉장고 = DB",
            "필요한 재료처럼\n데이터를 저장해 두는 곳이다.",
            "#f5f3ff",
            "#8b5cf6",
            "D",
        ),
    ]
    for item in boxes:
        card(draw, *item)

    for left, right in [(420, 460), (790, 830), (1160, 1200)]:
        arrow(draw, (left, 405), (right, 405), "#f59e0b", width=10, head=24)

    chip(draw, (100, 620), "1. 주문 받기", "#ef4444")
    chip(draw, (320, 620), "2. 로직 처리", "#f97316")
    chip(draw, (540, 620), "3. 데이터 확인", "#3b82f6")
    chip(draw, (760, 620), "4. 결과 응답", "#10b981")

    rounded(draw, (90, 700, 1510, 830), 28, "#fff1db", outline="#f59e0b", width=3)
    draw.text((124, 735), "한 줄 기억", font=font(28, bold=True), fill="#b45309")
    draw.text(
        (260, 734),
        "프론트는 주문하는 쪽, 백엔드는 주문을 실제로 처리하는 쪽, DB는 재료 창고다.",
        font=font(30, bold=True),
        fill="#78350f",
    )

    img.save(os.path.join(OUT_DIR, "01-restaurant-request-response.png"))


def create_localhost_port():
    img = Image.new("RGB", (1600, 920), "#f7fbff")
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((40, 40, 1560, 880), radius=36, fill="#ffffff", outline="#dbeafe", width=3)

    draw.text((90, 78), "localhost와 port는 주소 비유로 이해하면 덜 헷갈린다", font=font(54, bold=True), fill="#0f172a")
    draw.text(
        (92, 154),
        "localhost와 127.0.0.1은 같은 내 컴퓨터를 가리키지만, port가 달라지면 들어가는 문이 달라진다.",
        font=font(28),
        fill="#475569",
    )

    card(
        draw,
        (90, 250, 500, 470),
        "localhost",
        "사람 이름처럼 읽기 쉬운 이름표\n보통 \"내 컴퓨터\"를 뜻한다.",
        "#eff6ff",
        "#2563eb",
        "L",
    )
    card(
        draw,
        (90, 500, 500, 720),
        "127.0.0.1",
        "localhost가 가리키는 숫자 주소\n결국 둘 다 같은 집이다.",
        "#eefcf4",
        "#16a34a",
        "I",
    )

    rounded(draw, (700, 240, 1450, 760), 34, "#f8fafc", outline="#94a3b8", width=3)
    draw.text((760, 270), "내 컴퓨터(같은 집)", font=font(42, bold=True), fill="#1e293b")

    room_info = [
        ("3000", "프론트 개발 서버"),
        ("8080", "Spring Boot 서버"),
        ("3306", "MySQL 같은 DB 포트"),
    ]
    for idx, (port, desc) in enumerate(room_info):
        y = 360 + idx * 130
        rounded(draw, (880, y, 1280, y + 90), 20, "#dbeafe", outline="#60a5fa", width=2)
        draw.text((760, y + 18), port, font=font(36, bold=True), fill="#1d4ed8")
        draw.text((905, y + 18), desc, font=font(30, bold=True), fill="#1e293b")

    arrow(draw, (520, 360), (680, 360), "#f97316", width=10, head=22)
    arrow(draw, (520, 610), (680, 610), "#f97316", width=10, head=22)

    rounded(draw, (700, 790, 1450, 850), 20, "#eff6ff", outline="#2563eb", width=2)
    draw.text(
        (730, 804),
        "예) http://localhost:8080  ->  내 컴퓨터 안의 8080번 문으로 들어간다.",
        font=font(26, bold=True),
        fill="#1d4ed8",
    )

    rounded(draw, (90, 770, 590, 850), 20, "#fff7ed", outline="#f97316", width=2)
    draw_wrapped(
        draw,
        "주의: localhost와 127.0.0.1은 브라우저에서 다른 출처로 취급될 수 있어 CORS가 날 수 있다.",
        (118, 790, 560, 840),
        font(24, bold=True),
        "#9a3412",
        line_gap=4,
    )

    img.save(os.path.join(OUT_DIR, "02-localhost-port-address.png"))


def create_layered_architecture():
    img = Image.new("RGB", (1600, 980), "#f8fafc")
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((40, 40, 1560, 940), radius=36, fill="#ffffff", outline="#e2e8f0", width=3)

    draw.text((90, 76), "Spring Boot에서 요청이 흘러가는 길", font=font(54, bold=True), fill="#111827")
    draw.text(
        (92, 150),
        "MVC를 배웠다면, 실무에서는 보통 Controller -> Service -> Repository -> DB처럼 더 잘게 역할을 나눈다.",
        font=font(28),
        fill="#475569",
    )

    flow = [
        ((90, 300, 330, 500), "Front", "화면에서 버튼 클릭\n또는 폼 제출", "#dcfce7", "#16a34a"),
        ((390, 300, 650, 500), "Controller", "URL을 받고\n어느 서비스로 보낼지 결정", "#ffedd5", "#f97316"),
        ((710, 300, 970, 500), "Service", "진짜 비즈니스 규칙\n검사, 계산, 조합", "#fee2e2", "#ef4444"),
        ((1030, 300, 1290, 500), "Repository", "DB에서 읽고 쓰는\n전용 창구", "#e0e7ff", "#6366f1"),
        ((1350, 300, 1510, 500), "DB", "데이터 저장소", "#ede9fe", "#8b5cf6"),
    ]
    for box, title, subtitle, fill, accent in flow:
        rounded(draw, box, 28, fill, outline=accent, width=3)
        x1, y1, x2, y2 = box
        draw.text((x1 + 24, y1 + 22), title, font=font(36, bold=True), fill="#111827")
        draw_wrapped(draw, subtitle, (x1 + 24, y1 + 86, x2 - 24, y2 - 20), font(24), "#334155", line_gap=8)

    for left, right in [(330, 390), (650, 710), (970, 1030), (1290, 1350)]:
        arrow(draw, (left, 400), (right, 400), "#94a3b8", width=8, head=20)

    rounded(draw, (260, 590, 520, 770), 26, "#fff7ed", outline="#fb923c", width=3)
    draw.text((285, 618), "DTO = 배송 상자", font=font(34, bold=True), fill="#9a3412")
    draw_wrapped(
        draw,
        "프론트와 주고받을 데이터를\n필요한 모양으로 담는다.",
        (286, 675, 500, 760),
        font(24),
        "#7c2d12",
        line_gap=8,
    )

    rounded(draw, (1080, 590, 1510, 770), 26, "#eff6ff", outline="#60a5fa", width=3)
    draw.text((1106, 618), "왜 이렇게 나눌까?", font=font(34, bold=True), fill="#1d4ed8")
    points = [
        "- Controller: 입구 담당",
        "- Service: 규칙 담당",
        "- Repository: 저장 담당",
        "- 분리할수록 수정과 협업이 쉬워진다.",
    ]
    y = 670
    for item in points:
        draw.text((1110, y), item, font=font(22), fill="#1e3a8a")
        y += 34

    rounded(draw, (90, 820, 1510, 900), 24, "#fef3c7", outline="#f59e0b", width=2)
    draw.text(
        (120, 842),
        "비유로 기억하기: Controller는 입구 직원, Service는 주방장, Repository는 창고 담당, DB는 냉장고.",
        font=font(28, bold=True),
        fill="#92400e",
    )

    img.save(os.path.join(OUT_DIR, "03-spring-layered-architecture.png"))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    create_restaurant_flow()
    create_localhost_port()
    create_layered_architecture()
    print("generated:", OUT_DIR)
    for name in sorted(os.listdir(OUT_DIR)):
        print(name)


if __name__ == "__main__":
    main()
