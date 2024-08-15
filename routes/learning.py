from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from templates import templates

router = APIRouter()

@router.get("/learning", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("pages/learning.html", {"request": request})