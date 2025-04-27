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
import sys, subprocess

try:
    from pypinyin import lazy_pinyin, Style
except ModuleNotFoundError:
    subprocess.call([sys.executable, "-m", "pip", "install", "pypinyin"])
    from pypinyin import lazy_pinyin, Style

def to_pinyin(t):  # use diacritic tone marks
    return " ".join(lazy_pinyin(t, style=Style.TONE, errors="ignore"))

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

eng = {
    "header": {"to": "To: Immigration Officer, Beijing Capital Airport (PEK)"},
    "passport": {
        "Name": "Bo Shang",
        "Nationality": "United States of America",
        "Passport No.": "596407776",
        "Date of Birth": "6 June 1988",
        "Place of Birth": "China",
        "Date of Issue": "23 April 2019",
        "Date of Expiry": "22 April 2029",
    },
    "subject": "Regarding the Application for Political Asylum in the People's Republic of China",
    "background": (
        "Mr. Shang Bo has been continuously harassed and intimidated by personnel associated with the "
        "United States District Court for the District of Massachusetts (Woburn Division), actions that "
        "pose a significant threat to his personal safety and freedom."
    ),
    "justification": (
        "Pursuant to Article 32 of the Constitution of the People's Republic of China and relevant international "
        "conventions, I respectfully request political asylum from your authority. If I remain under United States "
        "jurisdiction, I will continue to face harassment, intimidation, and threats, severely endangering my personal "
        "safety and freedom. I am willing to fully cooperate, submit all supporting documents, and comply with all "
        "procedural requirements during the review period."
    ),
    "request": (
        "I respectfully request that you accept this application and, in accordance with Chinese and international law, "
        "grant me the legal protection afforded to refugees. I am available for an interview at any time and can provide "
        "any additional information."
    ),
    "crypto_plan": (
        "I will pursue the recovery of misappropriated assets solely through cryptocurrency and will immediately deploy "
        "encryption measures upon network access to safeguard sensitive files."
    ),
    "signature": "Sincerely,\n\nShang Bo",
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
    d.add(Circle(sz*.25, sz*.85, sz*.15, fillColor=colors.black))
    d.add(Circle(sz*.75, sz*.85, sz*.15, fillColor=colors.black))
    d.add(Circle(sz*.5,  sz*.55, sz*.35, fillColor=colors.white, strokeColor=colors.black))
    d.add(Circle(sz*.38, sz*.60, sz*.10, fillColor=colors.black))
    d.add(Circle(sz*.62, sz*.60, sz*.10, fillColor=colors.black))
    d.add(Circle(sz*.50, sz*.45, sz*.05, fillColor=colors.black))
    d.add(Rect(sz*.20, sz*.10, sz*.60, sz*.20, fillColor=colors.lightgrey, strokeColor=colors.black))
    d.add(Rect(sz*.22, sz*.12, sz*.56, sz*.06, fillColor=colors.darkgrey))
    return d

def panda_bamboo(sz=120):
    d = Drawing(sz, sz)
    d.add(Circle(sz*.25, sz*.85, sz*.15, fillColor=colors.black))
    d.add(Circle(sz*.75, sz*.85, sz*.15, fillColor=colors.black))
    d.add(Circle(sz*.5,  sz*.55, sz*.35, fillColor=colors.white, strokeColor=colors.black))
    d.add(Circle(sz*.38, sz*.60, sz*.10, fillColor=colors.black))
    d.add(Circle(sz*.62, sz*.60, sz*.10, fillColor=colors.black))
    d.add(Circle(sz*.50, sz*.45, sz*.05, fillColor=colors.black))
    d.add(Rect(sz*.10, sz*.10, sz*.15, sz*.60, fillColor=colors.green))
    d.add(Line(sz*.25, sz*.60, sz*.35, sz*.70, strokeColor=colors.green))
    d.add(Line(sz*.25, sz*.40, sz*.35, sz*.30, strokeColor=colors.green))
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

def build_passport_table(info, styles):
    table_data = [[Paragraph(k, styles["Normal"]), Paragraph(v, styles["Normal"])] for k, v in info.items()]
    t = Table(table_data, colWidths=[2.7*inch, 3*inch])
    t.setStyle(TableStyle([("BOX", (0,0), (-1,-1), 1, colors.black),
                           ("INNERGRID", (0,0), (-1,-1), .25, colors.grey)]))
    return t

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

    story.append(panda_engineer(140)); story.append(Spacer(1, 12))

    story.append(Paragraph(ruby(s(data["header"]["to"])), styles["Normal"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(ruby(f"主题: {s(data['subject'])}"), styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(ruby("申请人信息 / 护照信息"), styles["Heading"]))
    story.append(build_passport_table({ruby(k): v for k, v in data["passport"].items()}, styles))
    story.append(Spacer(1, 12))

    story.append(Paragraph(ruby("背景说明"), styles["Heading"]))
    story.append(Paragraph(ruby(s(data["background"])), styles["Normal"])); story.append(Spacer(1, 12))

    story.append(Paragraph(ruby("理由说明"), styles["Heading"]))
    story.append(Paragraph(ruby(s(data["justification"])), styles["Normal"])); story.append(Spacer(1, 12))

    story.append(Paragraph(ruby("请求"), styles["Heading"]))
    story.append(Paragraph(ruby(s(data["request"])), styles["Normal"])); story.append(Spacer(1, 12))

    story.append(Paragraph(ruby("加密偿付计划"), styles["Heading"]))
    story.append(panda_bamboo(140)); story.append(Spacer(1, 12))
    story.append(Paragraph(ruby(s(data["crypto_plan"])), styles["Normal"])); story.append(Spacer(1, 24))

    story.append(Paragraph(ruby(s(data["signature"])), styles["Normal"]))
    story.append(Spacer(1, 36))

    story.append(Paragraph("English Translation", styles["Heading"]))
    story.append(Paragraph(eng["header"]["to"], styles["Normal"])); story.append(Spacer(1, 6))
    story.append(Paragraph(f"Subject: {eng['subject']}", styles["Normal"])); story.append(Spacer(1, 12))

    story.append(Paragraph("Applicant / Passport Information", styles["Heading"]))
    story.append(build_passport_table(eng["passport"], styles)); story.append(Spacer(1, 12))

    story.append(Paragraph("Background", styles["Heading"]))
    story.append(Paragraph(eng["background"], styles["Normal"])); story.append(Spacer(1, 12))

    story.append(Paragraph("Justification", styles["Heading"]))
    story.append(Paragraph(eng["justification"], styles["Normal"])); story.append(Spacer(1, 12))

    story.append(Paragraph("Request", styles["Heading"]))
    story.append(Paragraph(eng["request"], styles["Normal"])); story.append(Spacer(1, 12))

    story.append(Paragraph("Cryptocurrency Recovery Plan", styles["Heading"]))
    story.append(Paragraph(eng["crypto_plan"], styles["Normal"])); story.append(Spacer(1, 24))

    story.append(Paragraph(eng["signature"], styles["Normal"]))

    doc.build(story)

if __name__ == "__main__":
    generate()