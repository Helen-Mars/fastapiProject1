from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import home, about

app = FastAPI()


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes
app.include_router(home.router)
app.include_router(about.router)