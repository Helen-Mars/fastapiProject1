from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# topic = []
@router.get("/travel/{topic}", name="travel")
async def travel(request: Request, topic: str):
    return templates.TemplateResponse("pages/travel.html", {
        "request": request,
        "topic": topic
    })


