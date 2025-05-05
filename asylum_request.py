# Disclaimer: The allegations presented here have not been adjudicated. They are
# included solely for illustrative legal-argument drafting. Consult qualified counsel
# before relying on or filing any portion of this document.

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
from reportlab.graphics.shapes import Drawing, Circle, Rect, Line, Ellipse, Polygon
import urllib.request
import sys, subprocess

try:
    from pypinyin import slug, Style
except ModuleNotFoundError:
    subprocess.call([sys.executable, "-m", "pip", "install", "pypinyin"])
    from pypinyin import slug, Style


def to_pinyin(text):
    return slug(text, style=Style.TONE, separator=" ", errors="ignore", strict=True).replace("u:", "ü")


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
        "MA District Court (Woburn Division), actions that "
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
    return t.replace("’", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")


def ruby(txt):
    return f"{txt}<br/><font size=8 color='grey'>({to_pinyin(txt)})</font>"


def panda_engineer(sz=160):
    d = Drawing(sz, sz)
    d.add(Ellipse(sz * 0.5, sz * 0.35, sz * 0.32, sz * 0.25, fillColor=colors.white, strokeColor=colors.black))
    d.add(Ellipse(sz * 0.28, sz * 0.18, sz * 0.12, sz * 0.08, fillColor=colors.black))
    d.add(Ellipse(sz * 0.72, sz * 0.18, sz * 0.12, sz * 0.08, fillColor=colors.black))
    d.add(Ellipse(sz * 0.25, sz * 0.35, sz * 0.09, sz * 0.06, fillColor=colors.black))
    d.add(Ellipse(sz * 0.75, sz * 0.35, sz * 0.09, sz * 0.06, fillColor=colors.black))
    d.add(Circle(sz * 0.5, sz * 0.7, sz * 0.3, fillColor=colors.white, strokeColor=colors.black))
    d.add(Circle(sz * 0.3, sz * 0.92, sz * 0.14, fillColor=colors.black))
    d.add(Circle(sz * 0.7, sz * 0.92, sz * 0.14, fillColor=colors.black))
    d.add(Ellipse(sz * 0.4, sz * 0.73, sz * 0.08, sz * 0.11, fillColor=colors.black))
    d.add(Ellipse(sz * 0.6, sz * 0.73, sz * 0.08, sz * 0.11, fillColor=colors.black))
    d.add(Circle(sz * 0.4, sz * 0.73, sz * 0.03, fillColor=colors.white))
    d.add(Circle(sz * 0.6, sz * 0.73, sz * 0.03, fillColor=colors.white))
    d.add(Circle(sz * 0.5, sz * 0.63, sz * 0.035, fillColor=colors.black))
    d.add(Line(sz * 0.5, sz * 0.61, sz * 0.48, sz * 0.57, strokeColor=colors.black))
    d.add(Line(sz * 0.5, sz * 0.61, sz * 0.52, sz * 0.57, strokeColor=colors.black))
    d.add(Rect(sz * 0.28, sz * 0.77, sz * 0.44, sz * 0.08, fillColor=colors.lightgrey, strokeColor=colors.black))
    d.add(Rect(sz * 0.24, sz * 0.77, sz * 0.52, sz * 0.03, fillColor=colors.darkgrey, strokeColor=None))
    for i in (0.36, 0.5, 0.64):
        d.add(Line(sz * i, sz * 0.77, sz * i, sz * 0.85, strokeColor=colors.black, strokeWidth=1))
    return d


def panda_bamboo(sz=160):
    d = Drawing(sz, sz)
    d.add(Ellipse(sz * 0.5, sz * 0.35, sz * 0.32, sz * 0.25, fillColor=colors.white, strokeColor=colors.black))
    d.add(Ellipse(sz * 0.28, sz * 0.18, sz * 0.12, sz * 0.08, fillColor=colors.black))
    d.add(Ellipse(sz * 0.72, sz * 0.18, sz * 0.12, sz * 0.08, fillColor=colors.black))
    d.add(Ellipse(sz * 0.25, sz * 0.35, sz * 0.09, sz * 0.06, fillColor=colors.black))
    d.add(Ellipse(sz * 0.75, sz * 0.35, sz * 0.09, sz * 0.06, fillColor=colors.black))
    d.add(Circle(sz * 0.5, sz * 0.7, sz * 0.3, fillColor=colors.white, strokeColor=colors.black))
    d.add(Circle(sz * 0.3, sz * 0.92, sz * 0.14, fillColor=colors.black))
    d.add(Circle(sz * 0.7, sz * 0.92, sz * 0.14, fillColor=colors.black))
    d.add(Ellipse(sz * 0.4, sz * 0.73, sz * 0.08, sz * 0.11, fillColor=colors.black))
    d.add(Ellipse(sz * 0.6, sz * 0.73, sz * 0.08, sz * 0.11, fillColor=colors.black))
    d.add(Circle(sz * 0.4, sz * 0.73, sz * 0.03, fillColor=colors.white))
    d.add(Circle(sz * 0.6, sz * 0.73, sz * 0.03, fillColor=colors.white))
    d.add(Circle(sz * 0.5, sz * 0.63, sz * 0.035, fillColor=colors.black))
    d.add(Line(sz * 0.5, sz * 0.61, sz * 0.48, sz * 0.57, strokeColor=colors.black))
    d.add(Line(sz * 0.5, sz * 0.61, sz * 0.52, sz * 0.57, strokeColor=colors.black))
    stalk_x = sz * 0.15
    segment_h = sz * 0.12
    for j in range(5):
        d.add(Rect(stalk_x, sz * 0.15 + j * segment_h, sz * 0.08, segment_h - 2, fillColor=colors.green, strokeColor=colors.darkgreen))
        d.add(Line(stalk_x, sz * 0.15 + j * segment_h, stalk_x + sz * 0.08, sz * 0.15 + j * segment_h, strokeColor=colors.darkgreen, strokeWidth=1))
    leaves = [
        [(stalk_x + sz * 0.08, sz * 0.55), (stalk_x + sz * 0.18, sz * 0.62), (stalk_x + sz * 0.11, sz * 0.66)],
        [(stalk_x + sz * 0.07, sz * 0.42), (stalk_x + sz * 0.17, sz * 0.35), (stalk_x + sz * 0.10, sz * 0.31)],
    ]
    for leaf in leaves:
        d.add(Polygon([coord for point in leaf for coord in point], fillColor=colors.green, strokeColor=colors.darkgreen))
    d.add(Ellipse(sz * 0.23, sz * 0.45, sz * 0.1, sz * 0.07, fillColor=colors.black))
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
    t = Table(table_data, colWidths=[2.7 * inch, 3 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ]
        )
    )
    return t


def add_legal_arguments(story, styles):
    prelim = (
        "The following arguments are drafted on the basis of allegations that remain unverified. "
        "They do not constitute a finding of fact and are provided for legal-theory discussion."
    )
    legal = [
        {
            "title": "I. T-Mobile’s Alleged Interference with Internet Access",
            "body": (
                "Under 47 U.S.C. § 201(b) and § 202(a) the Communications Act prohibits common carriers from engaging "
                "in unjust, unreasonable, or unreasonably discriminatory practices. Intentional throttling or denial "
                "of service, if proven, may therefore expose T-Mobile to injunctive relief and damages. Where such "
                "interference rises to intentional unauthorized access or damage to a protected computer system, "
                "the Computer Fraud and Abuse Act, 18 U.S.C. § 1030(g), provides a private civil cause of action "
                "for compensatory damages, injunctive relief, and attorney’s fees."
            ),
        },
        {
            "title": "II. Twitch: Cyber-Harassment and Religious Discrimination",
            "body": (
                "Twitch’s alleged targeted cyberattacks could support tort claims for intrusion upon seclusion and "
                "intentional infliction of emotional distress under state common law. Additionally, if Twitch’s "
                "content-moderation or messaging policies discriminate on the basis of religion, a claim could be "
                "brought under 42 U.S.C. § 2000a et seq. (public accommodations) or relevant state civil-rights "
                "statutes, subject to Twitch’s status as a place of public accommodation in the jurisdiction."
            ),
        },
        {
            "title": "III. Google: Antitrust and Tortious Interference",
            "body": (
                "Google’s alleged use of market power in AI to exclude or penalize developers may constitute "
                "monopolization or attempted monopolization under § 2 of the Sherman Act, 15 U.S.C. § 2. A plaintiff "
                "must show (1) monopoly power in a relevant market and (2) exclusionary conduct. If counsel "
                "were to advance arguments that knowingly contradict controlling precedent, such conduct could be "
                "sanctionable under Fed. R. Civ. P. 11(c) and may invite a court’s contempt powers. Related common-law "
                "claims include tortious interference with prospective economic advantage."
            ),
        },
        {
            "title": "IV. Authorization to Satisfy Judgment via Cryptographic Assets",
            "body": (
                "Federal courts possess equitable power to fashion remedies that include the turnover of assets "
                "in any form capable of satisfying a money judgment. Fed. R. Civ. P. 69(a) incorporates state "
                "collection procedures, many of which (e.g., Wyo. Stat. § 34-29-101) expressly recognize "
                "cryptocurrency as property. Executive Order 14067 and the Treasury’s 2023 ‘Illicit Finance Risk "
                "Assessment of Decentralized Finance’ acknowledge digital assets as lawful mediums of exchange. "
                "Accordingly, a court may order defendants—or the United States in a Federal Tort Claims Act action, "
                "28 U.S.C. §§ 1346(b), 2671-80—to satisfy an award through transfer of designated cryptocurrency "
                "to a court-controlled wallet, provided such transfer complies with 31 C.F.R. pt. 1010 (FinCEN) and "
                "OFAC sanctions programs."
            ),
        },
    ]
    story.append(Spacer(1, 24))
    story.append(Paragraph("Legal Arguments", styles["Heading"]))
    story.append(Paragraph(prelim, styles["Normal"]))
    story.append(Spacer(1, 12))
    for sec in legal:
        story.append(Paragraph(sec["title"], styles["Heading"]))
        story.append(Paragraph(sec["body"], styles["Normal"]))
        story.append(Spacer(1, 12))


def generate(filename="Bo_Shang_Asylum_Request_CN_PY.pdf"):
    base_font = register_font()
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=72, rightMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    styles["Normal"].fontName = base_font
    styles.add(ParagraphStyle(name="Heading", fontName=base_font, fontSize=12, spaceAfter=6))
    story = []

    story.append(panda_engineer(160))
    story.append(Spacer(1, 12))

    utc = datetime.now(timezone.utc)
    loc = utc.astimezone(ZoneInfo("Asia/Shanghai"))
    story.append(Paragraph(f"协调世界时: {utc:%Y-%m-%d %H:%M:%S} UTC", styles["Normal"]))
    story.append(Paragraph(f"当地时间: {loc:%Y-%m-%d %H:%M:%S} {loc.tzname()} (时区: {loc.tzinfo.key})", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(ruby(s(data["header"]["to"])), styles["Normal"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(ruby(f"主题: {s(data['subject'])}"), styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(ruby("申请人信息 / 护照信息"), styles["Heading"]))
    story.append(build_passport_table({ruby(k): v for k, v in data["passport"].items()}, styles))
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
    story.append(panda_bamboo(160))
    story.append(Spacer(1, 12))
    story.append(Paragraph(ruby(s(data["crypto_plan"])), styles["Normal"]))
    story.append(Spacer(1, 24))

    story.append(Paragraph(ruby(s(data["signature"])), styles["Normal"]))
    story.append(Spacer(1, 36))

    story.append(Paragraph("English Translation", styles["Heading"]))
    story.append(Paragraph(eng["header"]["to"], styles["Normal"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"Subject: {eng['subject']}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Applicant / Passport Information", styles["Heading"]))
    story.append(build_passport_table(eng["passport"], styles))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Background", styles["Heading"]))
    story.append(Paragraph(eng["background"], styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Justification", styles["Heading"]))
    story.append(Paragraph(eng["justification"], styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Request", styles["Heading"]))
    story.append(Paragraph(eng["request"], styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Cryptocurrency Recovery Plan", styles["Heading"]))
    story.append(Paragraph(eng["crypto_plan"], styles["Normal"]))
    story.append(Spacer(1, 24))

    story.append(Paragraph(eng["signature"], styles["Normal"]))

    add_legal_arguments(story, styles)

    doc.build(story)


if __name__ == "__main__":
    generate()