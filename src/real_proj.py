import fitz
import io
from django.conf import settings
from num2words import num2words

import os
import tempfile
from django.core.files.base import ContentFile
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from datetime import datetime 
from utils.generic import random_digits
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

def generate_unsigned_alnatour_contract(fields, language='A'):
    # Construct absolute input PDF path
    input_pdf_path = settings.BASE_DIR / 'applications' / 'contracts' / ('arabic.pdf' if language == 'A' else 'english.pdf')

    # Ensure the PDF file exists
    if not input_pdf_path.exists():
        raise FileNotFoundError(f"PDF not found at {input_pdf_path}")

    # Open the input PDF using absolute path string
    doc = fitz.open(str(input_pdf_path.resolve()))
    
    # Load Arabic font
    arabic_font_path = settings.BASE_DIR / 'applications' / 'contracts' / 'font' / 'font.otf'# don,t forget to put font file

    # Ensure the PDF has pages
    if doc.page_count == 0:
        raise ValueError("The input PDF has no pages or failed to open correctly.")
    
    fields = reverse_words_in_fields(fields,['client_name', 'alnatour_fees_words', 'client_name_page3'])
    # Define fields with their coordinates AND page numbers
    if language == "A":
        field_definitions = {
            "day": {"page": 0, "x": 436, "y": 212},
            "date": {"page": 0, "x": 345, "y": 212},
            "id_number": {"page": 0, "x": 120, "y": 327},
            "mobile_number": {"page": 0, "x": 389, "y": 357},
            "client_name": {"page": 0, "x": 350, "y": 329},
            "address": {"page": 0, "x": 250, "y": 357},
            "alnatour_fees_page_1": {"page": 1, "x": 133, "y": 241},
            "application_id_page_2": {"page": 1, "x": 125, "y": 286},
            "application_id_page_3": {"page": 2, "x": 265, "y": 166},
            "creation_date": {"page": 2, "x": 395, "y": 208},
            "alnatour_fees_page_3": {"page": 2, "x": 448, "y": 229},
            "alnatour_fees_words": {"page": 2, "x": 380, "y": 249},
            "alnatour_fees_page_3_2": {"page": 2, "x": 176, "y": 311},
            "due_date": {"page": 2, "x": 415, "y": 355},
            "client_name_page3": {"page": 2, "x": 380, "y": 480},
            "client_national_id_page3": {"page": 2, "x": 400, "y": 500},
            "client_location_page3": {"page": 2, "x": 430, "y": 520},
        }
    else:
        field_definitions = {
            "day": {"page": 0, "x": 149, "y": 205},
            "date": {"page": 0, "x": 256, "y": 205},
            "client_name": {"page": 0, "x": 115, "y": 322.5},
            "id_number": {"page": 0, "x": 248, "y": 323},
            "mobile_number": {"page": 0, "x": 360, "y": 323},
            "address": {"page": 0, "x": 455, "y": 322},
            "alnatour_fees_page_1": {"page": 0, "x": 291, "y": 604},
            "application_id_page_2": {"page": 1, "x": 278, "y": 95},
            "application_id_page_3": {"page": 2, "x": 146, "y": 159},
            "creation_date": {"page": 2, "x": 155, "y": 176},
            "alnatour_fees_page_3": {"page": 2, "x": 126, "y": 192},
            "alnatour_fees_words": {"page": 2, "x": 162, "y": 209},
            "alnatour_fees_page_3_2": {"page": 2, "x": 402, "y": 276},
            "due_date": {"page": 2, "x": 319, "y": 293},
            "client_name_page3": {"page": 2, "x": 140, "y": 410},
            "client_national_id_page3": {"page": 2, "x": 160, "y": 435},
            "client_location_page3": {"page": 2, "x": 112, "y": 458},
        }
    font_size = 15 if language == "A" else 12
    font_color = (0, 0, 0)  # Black color (RGB)

    # Try to load the Arabic font if it exists
    font_name = None
    if arabic_font_path.exists():
        try:
            # Load the font into PyMuPDF
            font_buffer = open(str(arabic_font_path), "rb").read()
            font_name = "arabic-font"
            # Insert the font into the document
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                page.insert_font(fontname=font_name, fontbuffer=font_buffer)
        except Exception as e:
            print(f"Warning: Could not load Arabic font: {e}")
            font_name = None

    # Process and insert text into PDF
    for field_name, text in fields.items():
        if field_name in field_definitions:
            field = field_definitions[field_name]
            
            # Convert text to string
            text_str = str(text)
            
            # Handle Arabic text processing
            if any(ord(c) > 127 for c in text_str):
                try:
                    # Reshape Arabic text to handle connected letters
                    reshaped_text = reshape(text_str)
                    # Apply bidirectional algorithm for proper display
                    display_text = get_display(reshaped_text)
                except Exception as e:
                    print(f"Warning: Arabic text processing failed for '{text_str}': {e}")
                    display_text = text_str
            else:
                display_text = text_str
            
            # Load correct page
            page = doc.load_page(field["page"])
            
            # Insert text with appropriate font
            try:
                if font_name:
                    # Use the loaded Arabic font
                    page.insert_text(
                        (field["x"], field["y"]), 
                        display_text, 
                        fontname=font_name,
                        fontsize=font_size, 
                        color=font_color
                    )
                else:
                    # Use default font (fallback)
                    page.insert_text(
                        (field["x"], field["y"]), 
                        display_text, 
                        fontsize=font_size, 
                        color=font_color
                    )
            except Exception as e:
                print(f"Warning: Failed to insert text '{display_text}' at field '{field_name}': {e}")
                # Fallback: try with default font
                try:
                    page.insert_text(
                        (field["x"], field["y"]), 
                        display_text, 
                        fontsize=font_size, 
                        color=font_color
                    )
                except Exception as e2:
                    print(f"Error: Complete failure to insert text '{display_text}': {e2}")

    # Save to a bytes buffer
    pdf_bytes = doc.write()
    doc.close()

    if not pdf_bytes:
        raise ValueError("Generated PDF content is empty.")
    
    # client_name_Prelim_Contract_date.pdf
    # return ContentFile(pdf_bytes, name=f'{fields.get("client_name")}_Prelim_Contract_{datetime.now().strftime("%Y%m%d")}.pdf')
    #pdf_name = f"unsigned_alnatour_contract_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    # Determine contract type label based on language
    contract_type = "Prelim_Contract" 

    # Extract client name safely
    # client_name = fields.get("client_name", "").strip().replace(" ", "_")
    client_name = random_digits(4)

    # Prepare date (English: 20250101, Arabic: ٢٠٢٥٠١٠١)
    date_str = datetime.now().strftime("%Y%m%d")
    # if language == "A":
    #     # Convert 0-9 → Arabic numerals
    #     arabic_digits = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
    #     date_str = date_str.translate(arabic_digits)

    # Final PDF name
    pdf_name = f"{client_name}_{contract_type}_{date_str}.pdf"

    # Attach name to output file
    output = io.BytesIO(pdf_bytes)
    output.seek(0)
    output.name = pdf_name
    return output




def convert_number_to_words(alnatour_fees, language):
    """
    Convert number to  words
    Example: 10000 -> "عشرة آلاف"
    """
    return num2words(alnatour_fees, lang=language)



from datetime import datetime

def get_day_name(date_str, language='A'):
    """
    Returns the day name in Arabic or English
    :param date_str: Date string in format 'YYYY-MM-DD'
    :param language: 'ar' for Arabic, 'en' for English
    :return: Day name in the specified language
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    if language == 'A':
        arabic_weekdays = {
            0: 'الإثنين',
            1: 'الثلاثاء',
            2: 'الأربعاء',
            3: 'الخميس',
            4: 'الجمعة',
            5: 'السبت',
            6: 'الأحد'
        }
        return arabic_weekdays[date_obj.weekday()]
    else:  # Default to English
        english_weekdays = [
            'Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday'
        ]
        return english_weekdays[date_obj.weekday()]

# Example usage
# print(get_day_name("2025-08-03", 'ar'))  # Output: الأحد
# print(get_day_name("2025-08-03", 'en'))  # Output: Sunday

def get_client_property_address(application):
    from applications.models import Property
    properties = Property.objects.filter(application=application)
    if properties.exists():
        return properties.first().location
    return ''