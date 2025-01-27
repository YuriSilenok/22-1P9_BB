from app.models.drive import Drive
from app.schemas.drive import DriveCreate

def create_drive(drive: DriveCreate):
    db_drive = Drive.create(**drive.dict())
    return db_drive