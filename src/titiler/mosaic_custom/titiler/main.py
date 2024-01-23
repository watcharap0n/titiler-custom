"""app.

app/main.py

"""

from fastapi import FastAPI
from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers
from titiler.mosaic.errors import MOSAIC_STATUS_CODES

from .router import mosaic

app = FastAPI(
    title="Mosaic Custom",
    description="Custom mosaic backend.",
    version="0.1.0",
    # docs_url="/custom/docs",
    # redoc_url="/custom/redoc",
    # openapi_url="/custom/openapi.json",
)
app.include_router(mosaic.router)
add_exception_handlers(app, DEFAULT_STATUS_CODES)
add_exception_handlers(app, MOSAIC_STATUS_CODES)


# Health Check
@app.get("/healthz", tags=["Health Check"])
def ping():
    """Health check."""
    return {"ping": "pong!"}
