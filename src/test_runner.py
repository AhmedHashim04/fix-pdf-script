
from generator import generate_unsigned_alnatour_contract
from test_data import arabic_fields, english_fields
from utility import build_pdf_name

def save(pdf, name):
    name= build_pdf_name(name)
    with open(name, "wb") as f:
        f.write(pdf.read())
    print("✅ Generated:", name)

# Arabic dataset
pdf = generate_unsigned_alnatour_contract(arabic_fields, "A")
save(pdf[0],pdf[1]+"-(A)fields_(A)template")
pdf = generate_unsigned_alnatour_contract(arabic_fields, "E")
save(pdf[0],pdf[1]+"-(A)fields_(E)template")
# English dataset
pdf = generate_unsigned_alnatour_contract(english_fields, "A")
save(pdf[0],pdf[1]+"-(E)fields_(A)template")
pdf = generate_unsigned_alnatour_contract(english_fields, "E")
save(pdf[0],pdf[1]+"-(E)fields_(E)template")