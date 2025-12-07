
import io
import fitz
from datetime import datetime
from pathlib import Path
from arabic_reshaper import reshape
from bidi.algorithm import get_display

BASE_DIR = Path(__file__).resolve().parent

def generate_unsigned_alnatour_contract(fields, language='A'):
    """
    Existing function from Al Natour project (replicated for test
    environment).
    You should:
    - keep the structure.
    - only adjust coordinates and filename logic.
    - NOT change production.
    """

    # Determine template
    pdf_path = BASE_DIR / "contracts" / ("arabic.pdf" if language =="A" else "english.pdf")
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF template not found: {pdf_path}")
    
    # Open document
    doc = fitz.open(str(pdf_path))


    # Load Arabic font
    arabic_font_path = BASE_DIR / "contracts" / "font" / "alfont_com_arial-1.ttf"
    font_name = None

    if arabic_font_path.exists():
        font_buffer = arabic_font_path.read_bytes()
        font_name = "arabic-font"
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            page.insert_font(fontname=font_name,
            fontbuffer=font_buffer)
    # Coordinate configuration (Same as production - initial baseline)
    if language == 'A':
            
        field_definitions = {
        "day": {"page": 0, "x": 445, "y": 212},
        "date": {"page": 0, "x": 345, "y": 212},
        "id_number": {"page": 0, "x": 144, "y": 327},
        "mobile_number": {"page": 0, "x": 389, "y": 357},
        "client_name": {"page": 0, "x": 410, "y": 329},
        "alnatour_fees_page_1": {"page": 1, "x": 129, "y": 241},
        "application_id_page_2": {"page": 1, "x": 133, "y": 286},
        "application_id_page_3": {"page": 2, "x": 275, "y": 166},
        "alnatour_fees_page_3": {"page": 2, "x": 394, "y": 230},
        "alnatour_fees_words": {"page": 2, "x": 381, "y": 246},
        "creation_date": {"page": 2, "x": 390, "y": 204},
        "alnatour_fees_page_3_2": {"page": 2, "x": 176, "y": 311},
        "client_name_page3": {"page": 2, "x": 428, "y": 480},
        "client_national_id_page3": {"page": 2, "x": 400, "y":
        500},"client_location_page3": {"page": 2, "x": 400, "y": 550},
        "due_date": {"page": 2, "x": 415, "y": 355},
        }

    else:
        field_definitions = {
        "day": {"page": 0, "x": 149, "y": 207},
        "date": {"page": 0, "x": 256, "y": 207},
        "id_number": {"page": 0, "x": 248, "y": 321},
        "mobile_number": {"page": 0, "x": 360, "y": 321},
        "client_name": {"page": 0, "x": 131, "y": 319},
        "alnatour_fees_page_1": {"page": 0, "x": 291, "y": 605},
        "address": {"page": 0, "x": 455, "y": 321},
        "application_id_page_3": {"page": 2, "x": 148, "y": 158},
        "alnatour_fees_page_3": {"page": 2, "x": 130, "y": 191},
        "alnatour_fees_words": {"page": 2, "x": 162, "y": 208},
        "creation_date": {"page": 2, "x": 159, "y": 175},
        "due_date": {"page": 2, "x": 319, "y": 291},
        "alnatour_fees_page_3_2": {"page": 2, "x": 402, "y": 276},
        "client_name_page3": {"page": 2, "x": 167, "y": 410},
        "client_national_id_page3": {"page": 2, "x": 160, "y": 435},
        "client_location_page3": {"page": 2, "x": 112, "y": 458},
        }

        font_size = 9 if language == 'A' else 8

    for key, value in fields.items():
        if key not in field_definitions:
            continue

        text = str(value)

    # Arabic shaping if needed

    if any(ord(c) > 127 for c in text):

        try:
            text = get_display(reshape(text))
        except:
            pass

        config = field_definitions[key]
        page = doc.load_page(config["page"])

    if font_name:
        page.insert_text(
            (config["x"], config["y"]),
            text,
            fontname=font_name,
            fontsize=font_size,
            color=(0, 0, 0)
        )
    else:
        page.insert_text(
            (config["x"], config["y"]),
            text,
            fontsize=font_size,
            color=(0, 0, 0)
        )

    # Save as memory file
    pdf_bytes = doc.write()
    doc.close()
    output = io.BytesIO(pdf_bytes)
    return output