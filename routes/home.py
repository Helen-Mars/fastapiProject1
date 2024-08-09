from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from templates import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("pages/home.html", {"request": request})
