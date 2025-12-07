import fitz

doc = fitz.open("./src/contracts/english.pdf")
page = doc.load_page(0)

for block in page.get_text("blocks"):
    print(block) 
    break
