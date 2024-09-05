from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import *
from routes import learning, home, about, work, cooperation

app = FastAPI()


# Mount static files

app.mount("/static/header", StaticFiles(directory="static/header"), name="header")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static/css", StaticFiles(directory="static/css"), name="css")
app.mount("/static/js", StaticFiles(directory="static/js"), name="js")
app.mount("/static/images", StaticFiles(directory="static/images"), name="images")
app.mount("/media", StaticFiles(directory="media"), name="media")

# Include routes
app.include_router(home.router)

app.include_router(learning.router)
app.include_router(work.router)
app.include_router(cooperation.router)
# app.include_router(display.router)
app.include_router(about.router)