from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Import routers from controllers
from controllers.health import router as health_router
from controllers.screenshots import router as screenshots_router

app = FastAPI(
    title="My Screenshot API",
    description="This API allows you to take screenshots of web pages and store them.",
    version="1.0.0",
    contact={
        "name": "Alejandro Diaz Roque",
        "url": "https://github.com/DiazRock",
        "email": "corolariodiaz@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Register the routers
app.include_router(health_router)
app.include_router(screenshots_router)

# Serve static files (e.g., screenshots)
app.mount("/static", StaticFiles(directory="/screenshots"), name="static")
