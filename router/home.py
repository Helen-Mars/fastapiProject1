from typing import Annotated
from fastapi import APIRouter, File, UploadFile, Query, HTTPException, Depends, Security
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy import func
from sqlmodel import select, Session
from starlette.requests import Request
from database import SessionDep
from templates import templates
from pathlib import Path
# from models import Hero, HeroPublic, HeroCreate, HeroUpdate, User, UserCreate, UserRead, UserLogin
from models import *
from utils import hash_password, verify_password, create_access_token, verify_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

MEDIA_DIR = Path("media")
project_dir = Path(__file__).parent.parent

lightbox_dir = project_dir / "static" / "images" / "photo_lightbox2"
lightbox_dir_thumb = project_dir / "static" / "images" / "photo_lightbox2_thumb"

image_data = []
image_data_thumb = []
for image_path in lightbox_dir.iterdir():
    if image_path.suffix.lower() in ('.jpg', '.jpeg', '.png'):
        image_data.append('photo_lightbox2/' + image_path.name)
        image_data_thumb.append('photo_lightbox2_thumb/' + image_path.name)

combined_images = list(zip(image_data, image_data_thumb))


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        return payload
    except HTTPException:
        raise HTTPException(status_code=403, detail="Not authenticated")








@router.post("/admin/approve/{message_id}")
async def approve_message(message_id: int, session: SessionDep):
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="留言不存在")
    message.is_approved = True
    session.add(message)
    session.commit()
    return {"status": "approved"}



@router.post("/messages")
async def post_message(msg: MessageCreate, session: SessionDep):
    new_message = Message(
        name=msg.name,
        title=msg.title,
        content=msg.content,
        parent_id=msg.parent_id,
        is_approved=True,
    )
    session.add(new_message)
    session.commit()
    session.refresh(new_message)
    return {"status": "waiting_approval"}


@router.get("/track_page")
async def track_page(db: SessionDep):
    page_view = db.exec(select(PageView)).first()
    if not page_view:
        page_view = PageView(count=1)
        db.add(page_view)
    else:
        page_view.count += 1

    db.commit()
    db.refresh(page_view)

    return {"message": "Page view recorded"}


@router.get("/page_view_count")
async def page_view_count(db: SessionDep):
    page_view = db.exec(select(PageView)).first()
    total_views = page_view.count if page_view else 0
    return {"total_views": total_views}


@router.get("/dashboard")
async def dashboard(current_user: dict = Depends(get_current_user)):
    if current_user['sub'] == 'admin':
        return {"message": "Welcome, Admin!", "role": "admin"}
    else:
        return {"message": "Welcome, User!", "role": "user"}


@router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"message": "You are logged in!", "user": current_user}


@router.post("/token")
async def login(user: UserLogin, db: SessionDep):
    statement = select(User).where(
        (User.username == user.username) |
        (User.email == user.email)
    )
    user_db = db.exec(statement).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, user_db.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token(data={"sub": user_db.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session:SessionDep):
    carousel_path = project_dir / "static" / "images" / "sunset"

    carousel_list = []
    for file in sorted(carousel_path.glob("*.jpg")):
        pic_path = request.url_for("images", path="/sunset/" + file.name)
        carousel_list.append(pic_path)


    messages = session.exec(
        select(Message).where(Message.is_approved == True).order_by(Message.create_at.desc())
    ).all()

    message_dict = {msg.id: msg.dict() for msg in messages}
    for msg in message_dict.values():
        msg["children"] = []

    roots = []
    for msg in message_dict.values():
        parent_id = msg["parent_id"]
        if parent_id is None or parent_id == 0:
            roots.append(msg)
        else:
            if parent_id in message_dict:
                parent_msg = message_dict[parent_id]
                msg["parent_name"] = parent_msg["name"]
                parent_msg["children"].append(msg)

    # print(carousel_list)
    return templates.TemplateResponse("pages/home.html", {
        "request": request,
        "images": combined_images,
        "carousel_list": carousel_list,
        "messages": roots})


@router.get("/register")
async def register(request: Request):
    html_file_path = project_dir / "static" / "html" / "register.html"
    return FileResponse(html_file_path)


@router.post("/register", response_model=UserRead)
async def resigter_user(user: UserCreate, session: SessionDep):  # type: ignore
    # statement = select(User).where((User.email == user.email) | (User.username == user.username))
    # db_user = session.exec(statement).first()
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Username or email already registered")
    user_dict = user.model_dump()
    user_dict['hashed_password'] = hash_password(user.password)
    db_user = User.model_validate(user_dict)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.post("/heroes/", response_model=HeroPublic)
async def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.get("/heroes/", response_model=list[HeroPublic])
async def read_heroes(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/heroes/{hero_id}", response_model=HeroPublic)
async def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.patch("/heroes/{hero_id}", response_model=HeroPublic)
async def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db


@router.delete("/heroes/{hero_id}")
async def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}

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
