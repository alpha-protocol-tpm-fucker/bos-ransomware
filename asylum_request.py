# fix: ensure Chinese glyphs render by using a built-in CJK font
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Circle, Rect, Line
import urllib.request

try:
    from pypinyin import pinyin, Style
    def to_pinyin(t):
        return " ".join("".join(x) for x in pinyin(t, style=Style.TONE3))
except Exception:
    def to_pinyin(t):
        return t

data = {
    "header": {"to": "首都机场（PEK）移民官员"},
    "passport": {
        "Name": "Bo Shang",
        "Nationality": "美利坚合众国",
        "Passport No.": "596407776",
        "Date of Birth": "1988年6月6日",
        "Place of Birth": "中国",
        "Date of Issue": "2019年4月23日",
        "Date of Expiry": "2029年4月22日",
    },
    "subject": "关于申请中华人民共和国政治庇护",
    "background": (
        "申请人尚博先生持续受到马萨诸塞州联邦地区法院（沃本分院）相关人员的骚扰和恐吓，"
        "这些行为对其人身安全和自由构成重大威胁。"
    ),
    "justification": (
        "本人依据《中华人民共和国宪法》第32条及相关国际公约，恳请贵方给予政治庇护。"
        "如继续处于美国司法管辖之下，我将面临持续骚扰、恐吓和威胁，"
        "严重危及我的人身安全与自由。我愿意充分配合，提交所有支持文件，"
        "并在审查期间遵守所有程序要求。"
    ),
    "request": (
        "恳请贵方受理本申请，并依据中国及国际法律赋予我作为难民的法律保护。"
        "我随时可接受面谈并提供任何额外信息。"
    ),
    "crypto_plan": (
        "我将仅以加密货币方式追索被侵占资产，并在接入网络后立即部署加密措施以保护敏感文件。"
    ),
    "signature": "此致\n\n尚博 敬上",
}

def s(t):
    return (
        t.replace("’", "'").replace("“", '"').replace("”", '"')
        .replace("–", "-").replace("—", "-")
    )

def ruby(txt):
    py = to_pinyin(txt)
    return f"{txt}<br/><font size=8 color='grey'>({py})</font>"

def panda_engineer(sz=120):
    d = Drawing(sz, sz)
    d.add(Circle(sz*0.25, sz*0.85, sz*0.15, fillColor=colors.black))
    d.add(Circle(sz*0.75, sz*0.85, sz*0.15, fillColor=colors.black))
    d.add(Circle(sz*0.5,  sz*0.55, sz*0.35, fillColor=colors.white, strokeColor=colors.black))
    d.add(Circle(sz*0.38, sz*0.60, sz*0.10, fillColor=colors.black))
    d.add(Circle(sz*0.62, sz*0.60, sz*0.10, fillColor=colors.black))
    d.add(Circle(sz*0.50, sz*0.45, sz*0.05, fillColor=colors.black))
    d.add(Rect(sz*0.20, sz*0.10, sz*0.60, sz*0.20, fillColor=colors.lightgrey, strokeColor=colors.black))
    d.add(Rect(sz*0.22, sz*0.12, sz*0.56, sz*0.06, fillColor=colors.darkgrey))
    return d

def panda_bamboo(sz=120):
    d = Drawing(sz, sz)
    d.add(Circle(sz*0.25, sz*0.85, sz*0.15, fillColor=colors.black))
    d.add(Circle(sz*0.75, sz*0.85, sz*0.15, fillColor=colors.black))
    d.add(Circle(sz*0.5,  sz*0.55, sz*0.35, fillColor=colors.white, strokeColor=colors.black))
    d.add(Circle(sz*0.38, sz*0.60, sz*0.10, fillColor=colors.black))
    d.add(Circle(sz*0.62, sz*0.60, sz*0.10, fillColor=colors.black))
    d.add(Circle(sz*0.50, sz*0.45, sz*0.05, fillColor=colors.black))
    d.add(Rect(sz*0.10, sz*0.10, sz*0.15, sz*0.60, fillColor=colors.green))
    d.add(Line(sz*0.25, sz*0.60, sz*0.35, sz*0.70, strokeColor=colors.green))
    d.add(Line(sz*0.25, sz*0.40, sz*0.35, sz*0.30, strokeColor=colors.green))
    return d

def register_font():
    try:
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        return "STSong-Light"
    except Exception:
        f = Path(__file__).with_name("DejaVuSansCondensed.ttf")
        if not f.exists():
            for u in (
                "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/version_2_37/ttf/DejaVuSansCondensed.ttf",
                "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSansCondensed.ttf",
            ):
                try:
                    urllib.request.urlretrieve(u, f)
                    break
                except Exception:
                    continue
        if f.exists():
            pdfmetrics.registerFont(TTFont("DejaVu", f.as_posix()))
            return "DejaVu"
        return "Helvetica"

def generate(filename="Bo_Shang_Asylum_Request_CN_PY.pdf"):
    base_font = register_font()
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=72, rightMargin=72,
                            topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    styles["Normal"].fontName = base_font
    styles.add(ParagraphStyle(name="Heading", fontName=base_font, fontSize=12, spaceAfter=6))
    story = []

    utc = datetime.now(timezone.utc)
    loc = utc.astimezone(ZoneInfo("Asia/Shanghai"))
    story.append(Paragraph(f"协调世界时: {utc:%Y-%m-%d %H:%M:%S} UTC", styles["Normal"]))
    story.append(Paragraph(f"当地时间: {loc:%Y-%m-%d %H:%M:%S} {loc.tzname()} (时区: {loc.tzinfo.key})", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(panda_engineer(140))
    story.append(Spacer(1, 12))

    story.append(Paragraph(ruby(s(data["header"]["to"])), styles["Normal"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(ruby(f"主题: {s(data['subject'])}"), styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(ruby("申请人信息 / 护照信息"), styles["Heading"]))
    labels = {
        "Name": "姓名",
        "Nationality": "国籍",
        "Passport No.": "护照号码",
        "Date of Birth": "出生日期",
        "Place of Birth": "出生地点",
        "Date of Issue": "签发日期",
        "Date of Expiry": "有效期至",
    }
    table_data = [
        [Paragraph(ruby(labels[k]), styles["Normal"]), Paragraph(v, styles["Normal"])]
        for k, v in data["passport"].items()
    ]
    t = Table(table_data, colWidths=[2.7*inch, 3*inch])
    t.setStyle(TableStyle([("BOX", (0,0), (-1,-1), 1, colors.black),
                           ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey)]))
    story.append(t)
    story.append(Spacer(1, 12))

    story.append(Paragraph(ruby("背景说明"), styles["Heading"]))
    story.append(Paragraph(ruby(s(data["background"])), styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(ruby("理由说明"), styles["Heading"]))
    story.append(Paragraph(ruby(s(data["justification"])), styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(ruby("请求"), styles["Heading"]))
    story.append(Paragraph(ruby(s(data["request"])), styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(ruby("加密偿付计划"), styles["Heading"]))
    story.append(panda_bamboo(140))
    story.append(Spacer(1, 12))
    story.append(Paragraph(ruby(s(data["crypto_plan"])), styles["Normal"]))
    story.append(Spacer(1, 24))

    story.append(Paragraph(ruby(s(data["signature"])), styles["Normal"]))

    doc.build(story)

if __name__ == "__main__":
    generate()