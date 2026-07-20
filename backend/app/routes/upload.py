from fastapi import APIRouter, UploadFile, File
from backend.app.services.pdf_service import save_pdf, extract_text_from_pdf

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        return {
            "status": "error",
            "message": "Only PDF files are allowed."
        }

    file_path = save_pdf(file)

    pdf_text = extract_text_from_pdf(file_path)

    return {
        "status": "success",
        "filename": file.filename,
        "text": pdf_text
    }