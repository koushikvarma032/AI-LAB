import re
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
PAN_PATTERN = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")
AADHAAR_PATTERN = re.compile(r"^\d{12}$")

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_filename_str(filename: str) -> str:
    return secure_filename(filename)

def validate_pan(pan: str) -> bool:
    if not pan:
        return False
    return bool(PAN_PATTERN.match(pan.strip().upper()))

def validate_aadhaar(aadhaar: str) -> bool:
    if not aadhaar:
        return False
    cleaned = "".join(aadhaar.split())
    return bool(AADHAAR_PATTERN.match(cleaned))
