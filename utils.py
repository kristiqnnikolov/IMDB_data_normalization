# utils.py
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil import parser
from countries import CORRECTIONS, STANDARD_COUNTRIES
from regex_date_spanish import convert_spanish_textdate_to_date_format
import re
from rapidfuzz import process


def fix_invalid_date(date_str):
    parts = date_str.split("-")
    if len(parts) != 3:
        return None

    a, b, c = parts

    if len(a) == 4:  # YYYY-MM-DD
        year = int(a)
        month = int(b)
        day = int(c)

        if month > 12:
            year += (month - 1) // 12
            month = (month - 1) % 12 + 1

    elif len(c) in (2, 4):  # DD-MM-YY or DD-MM-YYYY
        day = int(a)
        month = int(b)
        year = int(c)

        if len(c) == 2:
            year += 1900 if year >= 30 else 2000

    else:
        return None

    if not (1 <= month <= 12):
        return None

    while day > 28:
        try:
            return datetime(year, month, day).strftime("%Y-%m-%d")
        except ValueError:
            day -= 1

    try:
        return datetime(year, month, day).strftime("%Y-%m-%d")
    except ValueError:
        return None


def normalize_date(date_str):
    # Parse messy dates including numeric overflow, text, or Spanish text dates.
    # Returns a string in YYYY-MM-DD format or None if invalid.
    if pd.isna(date_str):
        return None
    date_str = str(date_str).strip()

    fixed = fix_invalid_date(date_str)
    if fixed:
        return fixed

    try:
        dt = parser.parse(date_str, dayfirst=False, yearfirst=False, fuzzy=True)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        try:
            dt = convert_spanish_textdate_to_date_format(date_str)
            return dt
        except Exception:
            return None


def normalize_content_rating(value):
    # Returns the rating if it is valid (R, PG, PG-13, G),
    # otherwise returns 'Unrated'.
    valid_ratings = ["R", "PG", "PG-13", "G"]
    if value not in valid_ratings:
        return "Unrated"
    return value


def normalize_usd_numbers(value):
    # Removes $, commas, letters
    # Converts to numeric
    value_str = str(value)
    value_str = re.sub(r"[^0-9]", "", value_str)  # keep only digits

    return float(value_str)


def normalize_rating(value):
    if pd.isnull(value):
        return None

    val = str(value).strip()  # remove spaces
    val = val.replace(",", ".")  # replace comma with dot
    val = val.replace(":", ".")  # replace double dots with dot

    # Remove everything except digits and dot
    val = re.sub(r"[^0-9.]", "", val)

    if val == "":
        return None

    # Keep only the first dot as decimal separator
    parts = val.split(".")
    if len(parts) == 1:
        return float(parts[0])
    else:
        return float(parts[0] + "." + parts[1])  # only first dot, ignore extra dots


def normalize_duration(value):
    # Invalid/missing entries are converted to np.nan
    try:
        return int(value)
    except (ValueError, TypeError):
        return "NaN"


def normalize_votes(value):
    if value is None:
        return np.nan
    try:
        # Remove dots, convert to int
        val_str = str(value).replace(".", "")
        return int(val_str)
    except (ValueError, TypeError):
        return np.nan


def normalize_title(value):
    if isinstance(value, str):
        try:
            return value.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return value
    return value


def normalize_country(name):
    if not isinstance(name, str):
        return name
    name = name.strip().replace(".", "").replace("1", "")  # remove dots and trailing 1
    name = CORRECTIONS.get(name, name)  # apply direct replacements
    # fuzzy match to standard countries
    match, score, _ = process.extractOne(name, STANDARD_COUNTRIES)
    return match if score >= 80 else name


def normalize_genre(value):
    # Cleans and normalizes a single genre string:
    # - Strips whitespace
    # - Standardizes capitalization
    # - Removes extra spaces around commas
    # - Sorts genres alphabetically
    if not isinstance(value, str):
        return value  # leave non-strings as-is

    value = value.strip()

    value = ", ".join([g.strip() for g in value.split(",")])

    value = value.title()

    value = ", ".join(sorted(value.split(", ")))

    return value
