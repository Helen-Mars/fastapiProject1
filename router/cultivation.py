from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from templates import templates
import json
from pathlib import Path

router = APIRouter()

# topic = "peace, elevate, enjoy"
@router.get("/self-cultivation/{topic}", name="cultivation")
async def cultivation_page(request: Request, topic: str):
    if topic == "peace":
        card_path = Path(__file__).parent.parent / "content/cultivation_card"
        audio_path = Path(__file__).parent.parent / "audio"

        card_list = []
        for file in sorted(card_path.glob("*.json")):
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                data["bg_image"] = request.url_for("images", path="/cultivation/"+data["bg_image"])
                data["audio_src"] = request.url_for("audio", path="/peace_music/"+data["audio_src"])

                card_list.append(data)

        return templates.TemplateResponse("pages/self-cultivation.html", {
            "request": request,
            "topic": topic,
            "cards": card_list
        })
    else:
        return templates.TemplateResponse("pages/self-cultivation.html", {
            "request": request,
            "topic": topic})

