import sys
import os
import uuid
from fastapi import APIRouter,File,UploadFile
from app.services.detect_pdf import analyze_pdf


router = APIRouter()

UPLOAD_DIR = 'app/storage/files'
os.makedirs(UPLOAD_DIR,exist_ok=True)


@router.post('/upload')
async def upload_document(file:File = File(...)):
    documnet_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR,f"{documnet_id}.pdf")

    with open(file_path,"wb") as f:
        f.write(await file.read())

    page_analysis = analyze_pdf(f)
    return {
        "document_id":documnet_id,
        "filename":file.filename,
        "pages":page_analysis,

    }
