from pathlib import Path
import shutil
import fitz

UPLOAD_FOLDER = Path("backend/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


def save_pdf(file):
    file_path = UPLOAD_FOLDER / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


def extract_text_from_pdf(pdf_path):
    text = ""

    document = fitz.open(pdf_path)

    for page in document:
        text += page.get_text()

    document.close()

    return text