
import re

def build_pdf_name(client_name: str):
    name = client_name.strip()
    name = re.sub(r'[\\/:*?"<>|]', '', name)
    name = " ".join(name.split())
    
    return f"Prelim Contract {name}.pdf"