import re
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.config import get_settings

SAFE_NAME = re.compile(r"^[\w.\- ]{1,180}$")
PNG_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
JPEG_MAGIC = bytes([0xFF, 0xD8])


def assert_safe_upload(file: UploadFile, raw: bytes) -> None:
    settings = get_settings()
    name = file.filename or ""
    if not SAFE_NAME.match(name):
        raise HTTPException(status_code=400, detail="bad filename")
    if len(raw) == 0:
        raise HTTPException(status_code=400, detail="empty file")
    if len(raw) > settings.max_upload_bytes:
        raise HTTPException(status_code=400, "file too large")
    mime = (file.content_type or "").split(";")[0].strip().lower()
    if mime not in settings.allowed_mime:
        raise HTTPException(status_code=400, detail=f"mime not allowed: {mime}")
    if mime == "image/png" and not raw.startswith(PNG_MAGIC):
        raise HTTPException(status_code=400, detail="png magic mismatch")
    if mime == "image/jpeg" and not raw.startswith(JPEG_MAGIC):
        raise HTTPException(status_code=400, detail="jpeg magic mismatch")


def store_bytes(ticket_id: int, filename: str, raw: bytes) -> Path:
    settings = get_settings()
    folder = Path(settings.upload_dir) / str(ticket_id)
    folder.mkdir(parents=True, exist_ok=True)
    clean = Path(filename).name
    dest = folder / clean
    dest.write_bytes(raw)
    return dest
