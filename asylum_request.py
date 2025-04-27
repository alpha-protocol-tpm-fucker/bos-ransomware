from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Circle, Rect, Line
import urllib.request

data = {
    "header": {"to": "Immigration Officer, Beijing Capital International Airport (PEK)"},
    "passport": {
        "Name": "Bo Shang",
        "Nationality": "United States of America",
        "Passport No.": "596407776",
        "Date of Birth": "06 Jun 1988",
        "Place of Birth": "China",
        "Date of Issue": "23 Apr 2019",
        "Date of Expiry": "22 Apr 2029",
    },
    "subject": "Request for Political Asylum in the People’s Republic of China",
    "background": (
        "Applicant, Mr. Bo Shang, has faced continual harassment and intimidation from "
        "officials associated with the MA District Court (Woburn Division). These actions "
        "pose a significant threat to his personal safety and freedom."
    ),
    "justification": (
        "I respectfully request asylum under Article 32 of the Constitution of the "
        "People’s Republic of China and relevant international conventions. I face "
        "continuous harassment, intimidation, and threats that place my safety and "
        "freedom at grave risk should I remain under U.S. jurisdiction. I am prepared "
        "to cooperate fully, submit all supporting documentation, and comply with all "
        "procedural requirements while my claim is examined."
    ),
    "request": (
        "Please accept this application and afford me the legal protections accorded "
        "to refugees under Chinese and international law. I am available for "
        "interviews and ready to provide any additional information required."
    ),
    "crypto_plan": (
        "I will seek repayment of misappropriated assets exclusively in cryptocurrency "
        "and will deploy encryption measures to protect sensitive files upon integration "
        "into the network."
    ),
    "signature": "Sincerely,\n\nBo Shang",
}

def s(t):
    return (
        t.replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("–", "-")
        .replace("—", "-")
    )

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
    f = Path(__file__).with_name("DejaVuSansCondensed.ttf")
    if not f.exists():
        urls = [
            "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/version_2_37/ttf/DejaVuSansCondensed.ttf",
            "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSansCondensed.ttf",
        ]
        for u in urls:
            try:
                urllib.request.urlretrieve(u, f)
                break
            except Exception:
                continue
    if f.exists():
        pdfmetrics.registerFont(TTFont("DejaVu", f.as_posix()))
        return "DejaVu"
    return "Helvetica"

def generate(filename="Bo_Shang_Asylum_Request.pdf"):
    base_font = register_font()
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=72, rightMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    styles["Normal"].fontName = base_font
    styles.add(ParagraphStyle(name="Heading", fontName="Helvetica-Bold", fontSize=12, spaceAfter=6))
    story = []

    utc = datetime.now(timezone.utc)
    loc = utc.astimezone(ZoneInfo("America/New_York"))
    story.append(Paragraph(f"UTC Time:   {utc:%Y-%m-%d %H:%M:%S} UTC", styles["Normal"]))
    story.append(Paragraph(f"Local Time: {loc:%Y-%m-%d %H:%M:%S} {loc.tzname()} (Time Zone: {loc.tzinfo.key})", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(panda_engineer(140))
    story.append(Spacer(1, 12))

    story.append(Paragraph(s(data["header"]["to"]), styles["Normal"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"Subject: {s(data['subject'])}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("APPLICANT DETAILS / PASSPORT INFORMATION", styles["Heading"]))
    labels = {
        "Name": "姓名",
        "Nationality": "国籍",
        "Passport No.": "护照号码",
        "Date of Birth": "出生日期",
        "Place of Birth": "出生地点",
        "Date of Issue": "签发日期",
        "Date of Expiry": "有效期至",
    }
    table_data = [[Paragraph(f"{k}/{labels.get(k,'')}", styles["Normal"]), Paragraph(v, styles["Normal"])] for k, v in data["passport"].items()]
    t = Table(table_data, colWidths=[2.7*inch, 3*inch])
    t.setStyle(TableStyle([("BOX", (0,0), (-1,-1), 1, colors.black), ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey)]))
    story.append(t)
    story.append(Spacer(1, 12))

    story.append(Paragraph("BACKGROUND", styles["Heading"]))
    story.append(Paragraph(s(data["background"]), styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("JUSTIFICATION", styles["Heading"]))
    story.append(Paragraph(s(data["justification"]), styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("REQUEST", styles["Heading"]))
    story.append(Paragraph(s(data["request"]), styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("CRYPTOGRAPHIC REPAYMENT PLAN", styles["Heading"]))
    story.append(panda_bamboo(140))
    story.append(Spacer(1, 12))
    story.append(Paragraph(s(data["crypto_plan"]), styles["Normal"]))
    story.append(Spacer(1, 24))

    story.append(Paragraph(s(data["signature"]), styles["Normal"]))

    doc.build(story)

if __name__ == "__main__":
    generate()