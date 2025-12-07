
import re

def build_pdf_name(client_name: str):
    print(client_name)
    name = client_name.strip()
    name = re.sub(r'[\\/:*?"<>|]', '', name)
    name = " ".join(name.split())
    
    return f"Prelim Contract {name}.pdf"

import re


arabic_pattern = re.compile(r'[\u0600-\u06FF]')

def is_arabic(text):
    return bool(arabic_pattern.search(text))

def reverse_words_in_fields(fields, keys_to_reverse):

    new_fields = fields.copy()
    for key in keys_to_reverse:
        if key in new_fields and isinstance(new_fields[key], str):
            value = new_fields[key]
            if is_arabic(value):
                words = value.split()   
                words.reverse()         
                new_fields[key] = " ".join(words)
    return new_fields
