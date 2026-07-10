import os
import shutil
from fastapi import HTTPException

from fastapi.responses import FileResponse

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.services.resume_service import ResumeService
from app.schemas.resume import ResumeResponse


router = APIRouter(
    prefix="/resumes",
    tags=["Resume"]
)


UPLOAD_DIR = "uploads/resumes"


@router.post(
    "/upload",
    response_model=ResumeResponse
)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )


    file_path = f"{UPLOAD_DIR}/{file.filename}"


    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )


    service = ResumeService(db)


    return service.create_resume(
        filename=file.filename,
        file_path=file_path,
        file_size=os.path.getsize(file_path),
        content_type=file.content_type,
        user_id=current_user.id
    )



@router.get("/my", response_model=list[ResumeResponse])
def my_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    service = ResumeService(db)

    return service.get_user_resumes(
        current_user.id
    )



@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    service = ResumeService(db)

    try:
        return service.delete_resume(
            resume_id,
            current_user.id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/{resume_id}/download")
def download_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    service = ResumeService(db)

    resume = service.get_resume_by_id(
        resume_id,
        current_user.id
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    if not os.path.exists(resume.file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return FileResponse(
        path=resume.file_path,
        filename=resume.filename,
        media_type=resume.content_type
    )
