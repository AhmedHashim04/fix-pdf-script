
from generator import generate_unsigned_alnatour_contract
from test_data import arabic_fields, english_fields
from utility import build_pdf_name

def save(pdf, name):
    with open(name, "wb") as f:
        f.write(pdf.read())
    print("✅ Generated:", name)

# Arabic dataset
pdf = generate_unsigned_alnatour_contract(arabic_fields, "A")
save(pdf, "AR_data_AR_template.pdf")
pdf = generate_unsigned_alnatour_contract(arabic_fields, "E")
save(pdf, "AR_data_EN_template.pdf")
# English dataset
pdf = generate_unsigned_alnatour_contract(english_fields, "A")
save(pdf, "EN_data_AR_template.pdf")
pdf = generate_unsigned_alnatour_contract(english_fields, "E")
save(pdf, "EN_data_EN_template.pdf")