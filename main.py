from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Import routers from controllers
from controllers.health import router as health_router
from controllers.screenshots import router as screenshots_router

app = FastAPI()

# Register the routers
app.include_router(health_router)
app.include_router(screenshots_router)

# Serve static files (e.g., screenshots)
app.mount("/static", StaticFiles(directory="/screenshots"), name="static")
