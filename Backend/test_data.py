from faker import Faker
import random, os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

fake = Faker()

INDIAN_BANKS = [
    {"name": "HDFC Bank Ltd", "swift": "HDFCINBB", "branch": "Fort Branch, Mumbai"},
    {"name": "State Bank of India", "swift": "SBININBB", "branch": "Main Branch, Delhi"},
    {"name": "ICICI Bank Ltd", "swift": "ICICINBB", "branch": "Nariman Point, Mumbai"},
    {"name": "Axis Bank Ltd", "swift": "UTIBINBB", "branch": "Connaught Place, Delhi"},
]

EUROPEAN_BANKS = [
    {"name": "Deutsche Bank AG", "swift": "DEUTDEDB", "branch": "Hamburg"},
    {"name": "BNP Paribas SA", "swift": "BNPAFRPP", "branch": "Paris"},
    {"name": "HSBC Bank plc", "swift": "MIDLGB22", "branch": "London"},
    {"name": "ING Bank NV", "swift": "INGBNL2A", "branch": "Amsterdam"},
]

INDIAN_COMPANIES = [
    {"name": "Bharat Machinery Imports Pvt Ltd", "address": "14 Industrial Estate, Pune 411001, India"},
    {"name": "Tata International Ltd", "address": "Bombay House, 24 Homi Mody St, Mumbai 400001, India"},
    {"name": "Reliance Trading Corporation", "address": "Maker Chambers IV, Nariman Point, Mumbai 400021, India"},
    {"name": "Hindustan Steel Components Ltd", "address": "Sector 18, Gurugram 122015, Haryana, India"},
]

EUROPEAN_COMPANIES = [
    {"name": "Schäfer Industrietechnik GmbH", "address": "Hauptstraße 22, Hamburg 20095, Germany"},
    {"name": "Müller Precision Engineering AG", "address": "Bahnhofstrasse 10, Zurich 8001, Switzerland"},
    {"name": "Renault Industrial Components SAS", "address": "15 Rue de la Paix, Paris 75002, France"},
    {"name": "Phillips Manufacturing BV", "address": "Eindhoven 5611, Netherlands"},
]

INDIAN_PORTS = [
    "Nhava Sheva (JNPT), Mumbai, India",
    "Chennai Port, Tamil Nadu, India",
    "Mundra Port, Gujarat, India",
    "Kolkata Port, West Bengal, India",
]

EUROPEAN_PORTS = [
    "Hamburg, Germany",
    "Rotterdam, Netherlands",
    "Antwerp, Belgium",
    "Felixstowe, United Kingdom",
]

GOODS_CATALOG = [
    {
        "description": "Industrial CNC Milling Machines, Model XR-500",
        "quantity": "5 units",
        "hs_code": "8457.10",
        "origin_cert": "German Chamber of Commerce"
    },
    {
        "description": "Pharmaceutical Grade API — Paracetamol USP",
        "quantity": "2000 kg",
        "hs_code": "2924.29",
        "origin_cert": "Swiss Chamber of Commerce"
    },
    {
        "description": "Stainless Steel Seamless Pipes, Grade 316L",
        "quantity": "50 MT",
        "hs_code": "7304.41",
        "origin_cert": "Chamber of Commerce and Industry, Hamburg"
    },
    {
        "description": "Solar Panel Inverters, Model SunPro 3000",
        "quantity": "200 units",
        "hs_code": "8504.40",
        "origin_cert": "Netherlands Chamber of Commerce"
    },
]


def generate_transaction():
    issuing_bank   = random.choice(INDIAN_BANKS)
    advising_bank  = random.choice(EUROPEAN_BANKS)
    applicant      = random.choice(INDIAN_COMPANIES)
    beneficiary    = random.choice(EUROPEAN_COMPANIES)
    goods          = random.choice(GOODS_CATALOG)
    port_loading   = random.choice(EUROPEAN_PORTS)
    port_discharge = random.choice(INDIAN_PORTS)
    amount         = round(random.uniform(20000, 500000), 2)
    issue_date     = fake.date_between('-60d', '-30d')
    expiry_date    = issue_date + timedelta(days=90)
    ship_date      = issue_date + timedelta(days=60)
    lc_number      = f"LC-2024-{issuing_bank['swift'][:4]}-{random.randint(10000,99999)}"

    return {
        "lc_number":      lc_number,
        "issue_date":     issue_date.strftime("%Y-%m-%d"),
        "expiry_date":    expiry_date.strftime("%Y-%m-%d"),
        "ship_date":      ship_date.strftime("%Y-%m-%d"),
        "place_of_expiry":port_discharge.split(",")[0],
        "issuing_bank":   issuing_bank,
        "advising_bank":  advising_bank,
        "applicant":      applicant,
        "beneficiary":    beneficiary,
        "goods":          goods,
        "amount":         amount,
        "currency":       "USD",
        "port_loading":   port_loading,
        "port_discharge": port_discharge,
        "invoice_number": f"INV-2024-{random.randint(1000,9999)}",
        "bl_number":      f"BL-{fake.bothify('??######').upper()}",
        "pi_reference":   f"PI-2023-{random.randint(100,999)}",
        "draft_tenor":    random.choice(["AT SIGHT", "90 days sight", "60 days sight"]),
        "insured_amount": round(amount * 1.10, 2),
    }


# ─── PDF Styling helpers ────────────────────────────────────────────────────

DARK_BLUE   = colors.HexColor("#1B3A6B")
MID_BLUE    = colors.HexColor("#2E5FA3")
LIGHT_GREY  = colors.HexColor("#F4F6FA")
BORDER_GREY = colors.HexColor("#CCCCCC")
TEXT_BLACK  = colors.HexColor("#1A1A1A")

def get_styles():
    base = getSampleStyleSheet()
    styles = {
        "doc_title": ParagraphStyle("doc_title", fontSize=16, textColor=colors.white,
                                     fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=2),
        "doc_subtitle": ParagraphStyle("doc_subtitle", fontSize=9, textColor=colors.HexColor("#AACCFF"),
                                        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=0),
        "section_head": ParagraphStyle("section_head", fontSize=9, textColor=DARK_BLUE,
                                        fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=3),
        "field_label": ParagraphStyle("field_label", fontSize=8, textColor=colors.HexColor("#555555"),
                                       fontName="Helvetica-Bold"),
        "field_value": ParagraphStyle("field_value", fontSize=9, textColor=TEXT_BLACK,
                                       fontName="Helvetica"),
        "normal": ParagraphStyle("normal_custom", fontSize=9, textColor=TEXT_BLACK,
                                  fontName="Helvetica", spaceAfter=4),
        "small": ParagraphStyle("small", fontSize=7.5, textColor=colors.HexColor("#555555"),
                                  fontName="Helvetica"),
        "footer": ParagraphStyle("footer", fontSize=7, textColor=colors.HexColor("#888888"),
                                  fontName="Helvetica", alignment=TA_CENTER),
        "amount": ParagraphStyle("amount", fontSize=13, textColor=DARK_BLUE,
                                  fontName="Helvetica-Bold", alignment=TA_CENTER),
    }
    return styles


def header_table(doc_type, swift_ref, styles):
    """Returns a banner table as the document header."""
    header_data = [[
        Paragraph(doc_type, styles["doc_title"]),
        Paragraph(f"SWIFT Format: {swift_ref}", styles["doc_subtitle"]) if swift_ref else Paragraph("", styles["doc_subtitle"])
    ]]
    t = Table(header_data, colWidths=[120*mm, 60*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), DARK_BLUE),
        ("SPAN",         (0, 0), (-1, -1)),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",   (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
    ]))
    return t


def kv_table(rows, styles):
    """2-col label/value table."""
    data = [[Paragraph(lbl, styles["field_label"]), Paragraph(val, styles["field_value"])]
            for lbl, val in rows]
    t = Table(data, colWidths=[55*mm, 115*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (0, -1), LIGHT_GREY),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("GRID",         (0, 0), (-1, -1), 0.4, BORDER_GREY),
    ]))
    return t


def two_party_table(left_label, left_lines, right_label, right_lines, styles):
    left_content  = Paragraph("<b>" + left_label  + "</b><br/>" + "<br/>".join(left_lines),  styles["field_value"])
    right_content = Paragraph("<b>" + right_label + "</b><br/>" + "<br/>".join(right_lines), styles["field_value"])
    t = Table([[left_content, right_content]], colWidths=[85*mm, 85*mm])
    t.setStyle(TableStyle([
        ("BOX",          (0, 0), (-1, -1), 0.4, BORDER_GREY),
        ("INNERGRID",    (0, 0), (-1, -1), 0.4, BORDER_GREY),
        ("BACKGROUND",   (0, 0), (-1, -1), LIGHT_GREY),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
    ]))
    return t


def section(title, styles):
    return Paragraph(f"▌ {title}", styles["section_head"])


def footer_note(lc_number, doc_type, styles):
    return Paragraph(
        f"LC Reference: {lc_number}  |  {doc_type}  |  Generated for trade finance processing",
        styles["footer"]
    )


# ─── Document generators ────────────────────────────────────────────────────

def build_pdf(path, story):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=15*mm, bottomMargin=20*mm
    )
    doc.build(story)


def doc1_letter_of_credit(tx, folder, styles):
    story = []
    story.append(header_table("LETTER OF CREDIT", "MT700 — UCP 600", styles))
    story.append(Spacer(1, 6))

    story.append(kv_table([
        ("LC Number",       tx["lc_number"]),
        ("Date of Issue",   tx["issue_date"]),
        ("Date of Expiry",  tx["expiry_date"]),
        ("Place of Expiry", tx["place_of_expiry"]),
        ("Currency / Amount", f"{tx['currency']}  {tx['amount']:,.2f}"),
        ("Amount Tolerance","10% plus or minus"),
        ("Draft Tenor",     tx["draft_tenor"]),
        ("Partial Shipments","NOT ALLOWED"),
        ("Transhipment",    "NOT ALLOWED"),
        ("Applicable Rules","UCP 600"),
    ], styles))

    story.append(Spacer(1, 8))
    story.append(section("PARTIES", styles))
    story.append(two_party_table(
        "APPLICANT (Importer)",
        [tx["applicant"]["name"], tx["applicant"]["address"],
         f"SWIFT: {tx['issuing_bank']['swift']}"],
        "BENEFICIARY (Exporter)",
        [tx["beneficiary"]["name"], tx["beneficiary"]["address"],
         f"SWIFT: {tx['advising_bank']['swift']}"],
        styles
    ))
    story.append(Spacer(1, 5))
    story.append(two_party_table(
        "ISSUING BANK",
        [tx["issuing_bank"]["name"], tx["issuing_bank"]["branch"],
         f"SWIFT: {tx['issuing_bank']['swift']}"],
        "ADVISING BANK",
        [tx["advising_bank"]["name"], tx["advising_bank"]["branch"],
         f"SWIFT: {tx['advising_bank']['swift']}"],
        styles
    ))

    story.append(Spacer(1, 8))
    story.append(section("SHIPMENT DETAILS", styles))
    story.append(kv_table([
        ("Port of Loading",          tx["port_loading"]),
        ("Port of Discharge",        tx["port_discharge"]),
        ("Latest Date of Shipment",  tx["ship_date"]),
        ("Available With",           f"{tx['advising_bank']['name']} by negotiation"),
    ], styles))

    story.append(Spacer(1, 8))
    story.append(section("DESCRIPTION OF GOODS", styles))
    story.append(kv_table([
        ("Goods",           tx["goods"]["description"]),
        ("Quantity",        tx["goods"]["quantity"]),
        ("HS Code",         tx["goods"]["hs_code"]),
        ("PI Reference",    tx["pi_reference"]),
    ], styles))

    story.append(Spacer(1, 8))
    story.append(section("REQUIRED DOCUMENTS", styles))
    docs = [
        "1. Signed Commercial Invoice in triplicate",
        f"2. Full set of clean on-board Bill of Lading made out to order of {tx['issuing_bank']['name']}",
        "3. Packing List in duplicate",
        f"4. Certificate of Origin issued by {tx['goods']['origin_cert']}",
        "5. Insurance Certificate covering 110% of invoice value against All Risks",
        f"6. Bill of Exchange drawn on {tx['issuing_bank']['name']}",
        "7. Pre-shipment Inspection Certificate by SGS or equivalent",
    ]
    for d in docs:
        story.append(Paragraph(d, styles["normal"]))

    story.append(Spacer(1, 6))
    story.append(section("SPECIAL CONDITIONS", styles))
    story.append(Paragraph("All documents must be in English.", styles["normal"]))
    story.append(Paragraph("Documents must be presented within 21 days of shipment date.", styles["normal"]))
    story.append(Paragraph("All banking charges outside India are for beneficiary account.", styles["normal"]))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GREY))
    story.append(footer_note(tx["lc_number"], "Letter of Credit", styles))

    build_pdf(f"{folder}/document_1_letter_of_credit.pdf", story)


def doc2_commercial_invoice(tx, folder, styles):
    story = []
    story.append(header_table("COMMERCIAL INVOICE", "", styles))
    story.append(Spacer(1, 6))

    story.append(kv_table([
        ("Invoice Number", tx["invoice_number"]),
        ("Invoice Date",   tx["ship_date"]),
        ("LC Reference",   tx["lc_number"]),
    ], styles))

    story.append(Spacer(1, 8))
    story.append(section("SELLER & BUYER", styles))
    story.append(two_party_table(
        "SELLER",
        [tx["beneficiary"]["name"], tx["beneficiary"]["address"],
         f"SWIFT: {tx['advising_bank']['swift']}"],
        "BUYER",
        [tx["applicant"]["name"], tx["applicant"]["address"],
         f"SWIFT: {tx['issuing_bank']['swift']}"],
        styles
    ))

    story.append(Spacer(1, 8))
    story.append(section("GOODS & FINANCIAL DETAILS", styles))
    story.append(kv_table([
        ("Description",      tx["goods"]["description"]),
        ("HS Code",          tx["goods"]["hs_code"]),
        ("Quantity",         tx["goods"]["quantity"]),
        ("Country of Origin",tx["beneficiary"]["address"].split(",")[-1].strip()),
        ("Port of Loading",  tx["port_loading"]),
        ("Port of Discharge",tx["port_discharge"]),
        ("Vessel",           f"MV {fake.last_name()}"),
    ], styles))

    story.append(Spacer(1, 8))
    amt_table = Table([[
        Paragraph("TOTAL INVOICE AMOUNT", styles["field_label"]),
        Paragraph(f"{tx['currency']}  {tx['amount']:,.2f}", styles["amount"])
    ]], colWidths=[85*mm, 85*mm])
    amt_table.setStyle(TableStyle([
        ("BOX",         (0,0),(-1,-1), 1.2, MID_BLUE),
        ("BACKGROUND",  (0,0),(0,-1),  LIGHT_GREY),
        ("BACKGROUND",  (1,0),(1,-1),  colors.HexColor("#EBF2FF")),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("LEFTPADDING", (0,0),(-1,-1), 8),
    ]))
    story.append(amt_table)

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GREY))
    story.append(footer_note(tx["lc_number"], "Commercial Invoice", styles))
    build_pdf(f"{folder}/document_2_commercial_invoice.pdf", story)


def doc3_bill_of_lading(tx, folder, styles):
    story = []
    story.append(header_table("BILL OF LADING", "Clean On-Board", styles))
    story.append(Spacer(1, 6))

    story.append(kv_table([
        ("BL Number",    tx["bl_number"]),
        ("LC Reference", tx["lc_number"]),
        ("Date of Issue",tx["ship_date"]),
        ("Freight",      "PREPAID"),
        ("Clean On-Board","YES"),
    ], styles))

    story.append(Spacer(1, 8))
    story.append(section("PARTIES", styles))
    story.append(two_party_table(
        "SHIPPER",
        [tx["beneficiary"]["name"], tx["beneficiary"]["address"]],
        "CONSIGNEE",
        [f"To the order of {tx['issuing_bank']['name']}"],
        styles
    ))
    story.append(Spacer(1, 5))
    story.append(kv_table([
        ("Notify Party", f"{tx['applicant']['name']}, {tx['applicant']['address']}"),
        ("Vessel",       f"MV {fake.last_name()}"),
    ], styles))

    story.append(Spacer(1, 8))
    story.append(section("SHIPMENT", styles))
    story.append(kv_table([
        ("Port of Loading",  tx["port_loading"]),
        ("Port of Discharge",tx["port_discharge"]),
        ("Description",      tx["goods"]["description"]),
        ("Quantity",         tx["goods"]["quantity"]),
        ("HS Code",          tx["goods"]["hs_code"]),
    ], styles))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GREY))
    story.append(footer_note(tx["lc_number"], "Bill of Lading", styles))
    build_pdf(f"{folder}/document_3_bill_of_lading.pdf", story)


def doc4_packing_list(tx, folder, styles):
    story = []
    story.append(header_table("PACKING LIST", "", styles))
    story.append(Spacer(1, 6))

    total_pkgs   = random.randint(5, 50)
    gross_weight = random.randint(500, 10000)
    net_weight   = random.randint(400, gross_weight - 50)

    story.append(kv_table([
        ("LC Reference",    tx["lc_number"]),
        ("Invoice Reference",tx["invoice_number"]),
        ("Date",            tx["ship_date"]),
        ("Exporter",        tx["beneficiary"]["name"]),
        ("Importer",        tx["applicant"]["name"]),
        ("Goods",           tx["goods"]["description"]),
        ("Total Quantity",  tx["goods"]["quantity"]),
        ("Total Packages",  f"{total_pkgs} cartons"),
        ("Gross Weight",    f"{gross_weight} kg"),
        ("Net Weight",      f"{net_weight} kg"),
        ("Port of Loading", tx["port_loading"]),
        ("Port of Discharge",tx["port_discharge"]),
    ], styles))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GREY))
    story.append(footer_note(tx["lc_number"], "Packing List", styles))
    build_pdf(f"{folder}/document_4_packing_list.pdf", story)


def doc5_certificate_of_origin(tx, folder, styles):
    story = []
    story.append(header_table("CERTIFICATE OF ORIGIN", "", styles))
    story.append(Spacer(1, 6))

    story.append(kv_table([
        ("LC Reference",    tx["lc_number"]),
        ("Invoice Reference",tx["invoice_number"]),
        ("Exporter",        f"{tx['beneficiary']['name']}, {tx['beneficiary']['address']}"),
        ("Importer",        f"{tx['applicant']['name']}, {tx['applicant']['address']}"),
        ("Goods",           tx["goods"]["description"]),
        ("HS Code",         tx["goods"]["hs_code"]),
        ("Quantity",        tx["goods"]["quantity"]),
        ("Country of Origin",tx["beneficiary"]["address"].split(",")[-1].strip()),
        ("Certifying Body", tx["goods"]["origin_cert"]),
    ], styles))

    story.append(Spacer(1, 10))
    story.append(section("CERTIFICATION", styles))
    story.append(Paragraph(
        "We hereby certify that the goods described above originate from the country stated above "
        "and that the particulars given are true and correct.",
        styles["normal"]
    ))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GREY))
    story.append(footer_note(tx["lc_number"], "Certificate of Origin", styles))
    build_pdf(f"{folder}/document_5_certificate_of_origin.pdf", story)


def doc6_insurance_certificate(tx, folder, styles):
    story = []
    story.append(header_table("INSURANCE CERTIFICATE", "", styles))
    story.append(Spacer(1, 6))

    story.append(kv_table([
        ("LC Reference",   tx["lc_number"]),
        ("Policy Number",  f"POL-{random.randint(100000,999999)}"),
        ("Insured",        tx["applicant"]["name"]),
        ("Insurer",        f"{fake.company()} Insurance Co."),
        ("Goods",          tx["goods"]["description"]),
        ("Quantity",       tx["goods"]["quantity"]),
        ("Port of Loading",tx["port_loading"]),
        ("Port of Discharge",tx["port_discharge"]),
        ("Insured Amount", f"{tx['currency']} {tx['insured_amount']:,.2f}"),
        ("Coverage Type",  "All Risks"),
    ], styles))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "NOTE: Insured amount represents 110% of invoice value as per UCP 600.",
        styles["small"]
    ))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GREY))
    story.append(footer_note(tx["lc_number"], "Insurance Certificate", styles))
    build_pdf(f"{folder}/document_6_insurance_certificate.pdf", story)


def doc7_bill_of_exchange(tx, folder, styles):
    story = []
    story.append(header_table("BILL OF EXCHANGE", "", styles))
    story.append(Spacer(1, 6))

    story.append(kv_table([
        ("Draft Number",  f"DFT-{random.randint(1000,9999)}"),
        ("LC Reference",  tx["lc_number"]),
        ("Date",          tx["ship_date"]),
        ("Tenor",         tx["draft_tenor"]),
        ("Drawer",        tx["beneficiary"]["name"]),
        ("Drawee",        tx["issuing_bank"]["name"]),
        ("Amount",        f"{tx['currency']} {tx['amount']:,.2f}"),
        ("Pay to Order of",tx["advising_bank"]["name"]),
    ], styles))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GREY))
    story.append(footer_note(tx["lc_number"], "Bill of Exchange", styles))
    build_pdf(f"{folder}/document_7_bill_of_exchange.pdf", story)


def doc8_inspection_certificate(tx, folder, styles):
    story = []
    story.append(header_table("INSPECTION CERTIFICATE", "SGS International", styles))
    story.append(Spacer(1, 6))

    story.append(kv_table([
        ("LC Reference",     tx["lc_number"]),
        ("Invoice Reference",tx["invoice_number"]),
        ("Inspector",        "SGS International Inspection Services"),
        ("Inspection Date",  tx["ship_date"]),
        ("Goods",            tx["goods"]["description"]),
        ("Quantity Inspected",tx["goods"]["quantity"]),
        ("Result",           "PASSED"),
        ("Remarks",          "Goods found in full conformity with contract specifications and LC requirements."),
    ], styles))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GREY))
    story.append(footer_note(tx["lc_number"], "Inspection Certificate", styles))
    build_pdf(f"{folder}/document_8_inspection_certificate.pdf", story)


# ─── Main ───────────────────────────────────────────────────────────────────

tx     = generate_transaction()
folder = "test_transaction_pdfs"
os.makedirs(folder, exist_ok=True)

styles = get_styles()

doc1_letter_of_credit(tx, folder, styles)
doc2_commercial_invoice(tx, folder, styles)
doc3_bill_of_lading(tx, folder, styles)
doc4_packing_list(tx, folder, styles)
doc5_certificate_of_origin(tx, folder, styles)
doc6_insurance_certificate(tx, folder, styles)
doc7_bill_of_exchange(tx, folder, styles)
doc8_inspection_certificate(tx, folder, styles)

print("=" * 50)
print("PDFs generated successfully!")
print(f"Folder   : {folder}/")
print(f"LC Number: {tx['lc_number']}")
print(f"Amount   : {tx['currency']} {tx['amount']:,.2f}")
print(f"Goods    : {tx['goods']['description']}")
print(f"From     : {tx['port_loading']}")
print(f"To       : {tx['port_discharge']}")
print("=" * 50)