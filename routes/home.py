from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from starlette.requests import Request
from templates import templates
from pathlib import Path

router = APIRouter()

MEDIA_DIR = Path("media")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("pages/home.html", {"request": request})

# @router.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     file_location = MEDIA_DIR / file.filename
#     with open(file_location, "wb") as f:
#         f.write(file.file.read())
#
#
# @router.get("/media/{filename}")
# async def get_media_file(filename: str):
#     file_path = MEDIA_DIR / filename
#     if file_path.exists():
#         return FileResponse(file_path)
#     return {"error": "File not found"}
