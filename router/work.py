from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/work", response_class=HTMLResponse)
async def get_achievement(request: Request):
    publication_path = Path(__file__).parent.parent / "content" / "publication" / "publication.json"

    # 读取 JSON 文件
    with open(publication_path, 'r', encoding='utf-8') as f:
        publications = json.load(f)

    for publication in publications:
        publication["pdflink"] = f"/content/publication/pdf/{publication['pdflink']}"

    # 将修改后的 publications 传递到模板
    return templates.TemplateResponse("pages/work.html", {"request": request, "publications": publications})
