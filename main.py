from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import home, about, display

app = FastAPI()


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static/css", StaticFiles(directory="static/css"), name="css")
app.mount("/static/js", StaticFiles(directory="static/js"), name="js")
app.mount("/static/images", StaticFiles(directory="static/images"), name="images")

# Include routes
app.include_router(home.router)

app.include_router(display.router)
app.include_router(about.router)