
from fastapi import APIRouter, UploadFile, File
from backend.app.config import (
    CHUNKS_FILE,
    FAISS_INDEX_FILE
)

from backend.app.services.pdf_service import (
    save_pdf,
    extract_text_from_pdf
)

from backend.app.services.text_service import clean_text

from backend.app.services.chunk_service import chunk_text

from backend.app.services.embedding_service import (
    generate_embeddings,
    create_faiss_index,
    save_faiss_index,
    load_faiss_index
)

from backend.app.services.retrieval_service import (
    save_chunks,
    load_chunks
)


router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # --------------------------------------------------
    # Step 1: Check file type
    # --------------------------------------------------

    if file.content_type != "application/pdf":
        return {
            "status": "error",
            "message": "Only PDF files are allowed."
        }

    try:

        # --------------------------------------------------
        # Step 2: Save uploaded PDF
        # --------------------------------------------------

        file_path = save_pdf(file)

        # --------------------------------------------------
        # Step 3: Extract PDF text
        # --------------------------------------------------

        pdf_text = extract_text_from_pdf(file_path)

        if not pdf_text.strip():
            return {
                "status": "error",
                "message": "The PDF does not contain readable text."
            }

        # --------------------------------------------------
        # Step 4: Clean extracted text
        # --------------------------------------------------

        cleaned_text = clean_text(pdf_text)

        if not cleaned_text.strip():
            return {
                "status": "error",
                "message": "No usable text was found in the PDF."
            }

        # --------------------------------------------------
        # Step 5: Create chunks for the new PDF
        # --------------------------------------------------

        raw_chunks = chunk_text(cleaned_text)

        if not raw_chunks:
            return {
                "status": "error",
                "message": "Unable to create text chunks from the PDF."
            }

        # Add document metadata to every chunk
        new_chunks = [
            {
                "filename": file.filename,
                "text": chunk
            }
            for chunk in raw_chunks
        ]

        # --------------------------------------------------
        # Step 6: Load existing chunks
        # --------------------------------------------------

        chunks_path = CHUNKS_FILE

        try:
            existing_chunks = load_chunks(chunks_path)

        except FileNotFoundError:
            existing_chunks = []

        # --------------------------------------------------
        # Step 7: Check whether this PDF already exists
        # --------------------------------------------------

        existing_filenames = {
            chunk["filename"]
            for chunk in existing_chunks
            if isinstance(chunk, dict)
            and "filename" in chunk
        }

        if file.filename in existing_filenames:
            return {
                "status": "error",
                "message": f"{file.filename} has already been uploaded."
            }

        # --------------------------------------------------
        # Step 8: Combine old + new chunks
        # --------------------------------------------------

        all_chunks = existing_chunks + new_chunks

        # --------------------------------------------------
        # Step 9: Save all chunks
        # --------------------------------------------------

        save_chunks(
            all_chunks,
            chunks_path
        )

        # --------------------------------------------------
        # Step 10: Extract text for embeddings
        # --------------------------------------------------

        texts = [
            chunk["text"]
            for chunk in all_chunks
        ]

        # --------------------------------------------------
        # Step 11: Generate embeddings
        # --------------------------------------------------

        embeddings = generate_embeddings(texts)

        # --------------------------------------------------
        # Step 12: Create FAISS index
        # --------------------------------------------------

        index = create_faiss_index(embeddings)

        # --------------------------------------------------
        # Step 13: Save FAISS index
        # --------------------------------------------------

        faiss_path = FAISS_INDEX_FILE

        save_faiss_index(
            index,
            faiss_path
        )

        # --------------------------------------------------
        # Step 14: Load FAISS index again
        # --------------------------------------------------

        loaded_index = load_faiss_index(
            faiss_path
        )

        # --------------------------------------------------
        # Step 15: Return success response
        # --------------------------------------------------

        return {
            "status": "success",
            "filename": file.filename,
            "new_chunks": len(new_chunks),
            "total_chunks": len(all_chunks),
            "embedding_dimension": len(embeddings[0]),
            "vectors_stored": index.ntotal,
            "loaded_vectors": loaded_index.ntotal,
            "faiss_index": str(faiss_path),
            "message": (
                "PDF added successfully and FAISS index "
                "rebuilt using all documents."
            )
        }

    except Exception as e:

        print("Upload processing error:", e)

        return {
            "status": "error",
            "message": "Unable to process the uploaded PDF."
        }

