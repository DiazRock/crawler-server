from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Import routers from controllers
from controllers.health import router as health_router
from controllers.screenshots import router as screenshots_router
from controllers.metrics import router as metrics_router

# Import middlewares
from middlewares.prometheus_middleware import prometheus_middleware

load_dotenv()
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

need_expose_metrics = os.getenv('IS_EXPOSE_METRICS')
if need_expose_metrics == 'True':
    app.middleware("http")(prometheus_middleware)
    app.include_router(metrics_router)


app.middleware("http")(prometheus_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  # Specify the exact origin here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register the routers
app.include_router(health_router)
app.include_router(screenshots_router)


# Serve static files (e.g., screenshots)
scsh_path = os.getenv('SCREENSHOT_FOLDER')
app.mount(f"/{scsh_path}", 
          StaticFiles(directory=scsh_path), 
          name=scsh_path)
