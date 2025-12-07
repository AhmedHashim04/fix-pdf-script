import io
import fitz
from datetime import datetime
from pathlib import Path
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from utility import reverse_words_in_fields

BASE_DIR = Path(__file__).resolve().parent


def generate_unsigned_alnatour_contract(fields, language='A'):
    # Determine template
    pdf_path = BASE_DIR / "contracts" / ("arabic.pdf" if language == "A" else "english.pdf")
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF template not found: {pdf_path}")

    # Open document
    doc = fitz.open(str(pdf_path))

    # Load Arabic font
    arabic_font_path = BASE_DIR / "contracts" / "font" / "font.otf"
    font_name = None

    if arabic_font_path.exists():
        font_buffer = arabic_font_path.read_bytes()
        font_name = "arabic-font"

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            page.insert_font(fontname=font_name, fontbuffer=font_buffer)

    # Coordinates
    fields = reverse_words_in_fields(fields,['client_name', 'alnatour_fees_words', 'client_name_page3'])
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
            "alnatour_fees_page_3": {"page": 2, "x": 394, "y": 230},
            "alnatour_fees_page_3_2": {"page": 2, "x": 176, "y": 311},
            "creation_date": {"page": 2, "x": 390, "y": 204},
            "alnatour_fees_words": {"page": 2, "x": 375, "y": 247},
            "alnatour_fees_words_2": {"page": 2, "x": 375, "y": 333},
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
            "application_id_page_3": {"page": 2, "x": 148, "y": 158},
            "alnatour_fees_page_3": {"page": 2, "x": 130, "y": 191},
            "alnatour_fees_page_3_2": {"page": 2, "x": 402, "y": 276},
            "creation_date": {"page": 2, "x": 159, "y": 175},
            "alnatour_fees_words": {"page": 2, "x": 162, "y": 208},
            # "alnatour_fees_words_2": {"page": 2, "x": 452, "y": 276},
            "due_date": {"page": 2, "x": 319, "y": 293},
            "client_name_page3": {"page": 2, "x": 140, "y": 410},
            "client_national_id_page3": {"page": 2, "x": 160, "y": 435},
            "client_location_page3": {"page": 2, "x": 112, "y": 458},
        }

    font_size = 15 if language == "A" else 12

    # ------------- FIXED AREA (LOOP) -------------
    for key, value in fields.items():
        if key not in field_definitions:
            continue

        text = str(value)

        # Arabic shaping
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

    # Save
    pdf_bytes = doc.write()
    doc.close()

    return io.BytesIO(pdf_bytes),fields["client_name"]
