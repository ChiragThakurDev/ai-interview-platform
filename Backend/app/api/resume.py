import os
import shutil

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



@router.get(
    "/my",
    response_model=list[ResumeResponse]
)
def my_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    service = ResumeService(db)

    return service.get_user_resumes(
        current_user.id
    )
