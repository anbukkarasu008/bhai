from fastapi import APIRouter, UploadFile, File
from backend.app.services.pdf_service import save_pdf, extract_text_from_pdf
from backend.app.services.text_service import clean_text,chunk_text
from backend.app.services.embedding_service import generate_embeddings
from backend.app.services.embedding_service import (
    generate_embeddings,
    create_faiss_index,
    save_faiss_index,
    load_faiss_index
)

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
    embeddings = generate_embeddings(chunks)
    index = create_faiss_index(embeddings)
    save_faiss_index(index, "backend/vector_store/faiss_index.bin")
    loaded_index = load_faiss_index("backend/vector_store/faiss_index.bin")
    return {
    "status": "success",
    "filename": file.filename,
    "total_chunks": len(chunks),
    "embedding_dimension": len(embeddings[0]),
    "vectors_stored": index.ntotal,
    "loaded_vectors": loaded_index.ntotal,
    "faiss_index": "backend/vector_store/faiss_index.bin",
    "message": "FAISS index created, saved and loaded successfully."
}



