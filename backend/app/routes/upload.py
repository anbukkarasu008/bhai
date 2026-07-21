from fastapi import APIRouter, UploadFile, File
from backend.app.services.pdf_service import save_pdf, extract_text_from_pdf
from backend.app.services.text_service import clean_text,chunk_text

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
    cleaned_text = clean_text(pdf_text)

    chunks = chunk_text(cleaned_text)

    return {
        "status": "success",
        "filename": file.filename,
        "total_chunks": len(chunks),
        "chunks": chunks
}




