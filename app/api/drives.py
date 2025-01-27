from fastapi import APIRouter, Depends, HTTPException
from app.schemas.drive import DriveCreate, DriveResponse
from app.crud.drive import create_drive
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/drives/", response_model=DriveResponse)
async def create_drive_endpoint(
    drive: DriveCreate,
    current_user: dict = Depends(get_current_user),
):
    db_drive = create_drive(drive)
    return db_drive