from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from templates import templates
from enum import Enum

item = {
    "id": 1,
    "name": "Sample Item",
    "description": "This is a detailed description of the sample item.",
    "price": 19.99
}

router = APIRouter()

@router.get("/display", response_class=HTMLResponse)
async def display(request: Request):
    return templates.TemplateResponse("pages/display.html", {"request": request, "item": item})