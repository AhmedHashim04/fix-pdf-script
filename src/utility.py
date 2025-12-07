
import re

def build_pdf_name(client_name: str):
    name = client_name.strip()
    name = re.sub(r'[\\/:*?"<>|]', '', name)
    name = " ".join(name.split())
    
    return f"Prelim Contract {name}.pdf"

def reverse_words_in_fields(fields, keys_to_reverse):

    new_fields = fields.copy()
    for key in keys_to_reverse:
        if key in new_fields and isinstance(new_fields[key], str):
            words = new_fields[key].split()   
            words.reverse()                 
            new_fields[key] = " ".join(words) 
    return new_fields
