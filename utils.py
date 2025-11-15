import re

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
def is_valid_email(email):
    return re.match(EMAIL_REGEX, email) is not None

def is_zipcode_valid(zipcode):
    return zipcode.isdigit() and len(zipcode) == 5