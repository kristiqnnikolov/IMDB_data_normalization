# regex_date_spanish.py
import re


def convert_spanish_textdate_to_date_format(text):
    pattern = r"\b(\d{1,2}(?:st|nd|rd|th)?)\b.*?\b(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\b.*?\b(\d{4})\b"

    match = re.search(pattern, text, re.IGNORECASE)

    if not match:
        return None

    day_raw = match.group(1)
    month_raw = match.group(2)
    year = match.group(3)

    day_num = re.sub(r"(st|nd|rd|th)$", "", day_raw)
    day = day_num.zfill(2)

    months = {
        "enero": "01",
        "febrero": "02",
        "marzo": "03",
        "abril": "04",
        "mayo": "05",
        "junio": "06",
        "julio": "07",
        "agosto": "08",
        "septiembre": "09",
        "octubre": "10",
        "noviembre": "11",
        "diciembre": "12",
    }

    month = months[month_raw.lower()]

    formatted = f"{year}-{month}-{day}"
    return formatted
