from fpdf import FPDF
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
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

def s(txt):
    return (txt.replace("’", "'").replace("“", '"').replace("”", '"')
            .replace("–", "-").replace("—", "-"))

def add(pdf, txt=""):
    pdf.multi_cell(0, 9, s(txt))

def generate(filename="Bo_Shang_Asylum_Request.pdf"):
    pdf = FPDF(format="letter")
    pdf.add_page()
    pdf.set_auto_page_break(True, 15)
    pdf.set_font("Helvetica", size=11)

    fp = Path(__file__).with_name("DejaVuSansCondensed.ttf")
    cn_font = "Helvetica"
    if not fp.exists():
        try:
            url = (
                "https://github.com/dejavu-fonts/dejavu-fonts/raw/version_2_37/ttf/"
                "DejaVuSansCondensed.ttf"
            )
            urllib.request.urlretrieve(url, fp)
        except Exception:
            pass
    if fp.exists():
        pdf.add_font("DejaVu", "", fp.as_posix(), uni=True)
        cn_font = "DejaVu"

    utc = datetime.now(timezone.utc)
    loc = utc.astimezone(ZoneInfo("America/New_York"))

    add(pdf, f"UTC Time:   {utc:%Y-%m-%d %H:%M:%S} UTC")
    add(pdf, f"Local Time: {loc:%Y-%m-%d %H:%M:%S} {loc.tzname()}")
    add(pdf, f"Time Zone:  {loc.tzinfo.key}"); add(pdf)

    add(pdf, "Illustration: Panda Software Engineer"); add(pdf)
    add(pdf, data["header"]["to"]); add(pdf)
    add(pdf, f"Subject: {data['subject']}"); add(pdf)

    add(pdf, "APPLICANT DETAILS / PASSPORT INFORMATION")
    labels = {
        "Name": "姓名",
        "Nationality": "国籍",
        "Passport No.": "护照号码",
        "Date of Birth": "出生日期",
        "Place of Birth": "出生地点",
        "Date of Issue": "签发日期",
        "Date of Expiry": "有效期至",
    }

    y0 = pdf.get_y()
    lm = pdf.l_margin
    w = pdf.w - 2 * lm
    for k, v in data["passport"].items():
        lbl = f"{k}/{labels.get(k,'')}:" if cn_font != "Helvetica" else f"{k}:"
        pdf.set_font(cn_font, "B", 11)
        pdf.cell(65, 9, lbl)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 9, v, ln=1)
    pdf.rect(lm, y0 - 1, w, pdf.get_y() - y0 + 1); add(pdf)

    add(pdf, "BACKGROUND")
    add(pdf, data["background"]); add(pdf)

    add(pdf, "JUSTIFICATION")
    add(pdf, data["justification"]); add(pdf)

    add(pdf, "REQUEST")
    add(pdf, data["request"]); add(pdf)

    add(pdf, "CRYPTOGRAPHIC REPAYMENT PLAN")
    add(pdf, "Illustration: Panda Eating Bamboo"); add(pdf)
    add(pdf, data["crypto_plan"]); add(pdf)

    add(pdf, data["signature"])
    pdf.output(filename)

if __name__ == "__main__":
    generate()