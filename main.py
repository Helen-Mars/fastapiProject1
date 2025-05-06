from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import lifespan
from router import home, learning, work, cooperation, about, cultivation, travel

app = FastAPI(lifespan=lifespan)
app.state.global_variables = {
    "svg_path": "/static/svgs/icons.svg",
}

# Mount static files

app.mount("/static/bootstrap", StaticFiles(directory="static/bootstrap"), name="bootstrap")
app.mount("/static/lightbox2", StaticFiles(directory="static/lightbox2"), name="lightbox2")
app.mount("/static/svgs", StaticFiles(directory="static/svgs"), name="svgs")

app.mount("/static/css", StaticFiles(directory="static/css"), name="css")
app.mount("/static/js", StaticFiles(directory="static/js"), name="js")
app.mount("/static/images", StaticFiles(directory="static/images"), name="images")
app.mount("/audio", StaticFiles(directory="audio"), name="audio")
app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/content/publication/pdf", StaticFiles(directory="content/publication/pdf"), name="content_publication_pdf")

# Include routes
app.include_router(home.router)
app.include_router(learning.router)
app.include_router(work.router)
app.include_router(cooperation.router)
app.include_router(about.router)
app.include_router(cultivation.router, prefix="/cultivation", tags=["Cultivation"])
app.include_router(travel.router, prefix="/travel", tags=["Travel"])


