from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .config import PUBLIC_DIR, settings
from .database import Base, engine, ensure_sqlite_schema
from .routers import audio, auth, dictionary, health, hosts, profile, progress, search, stories


app = FastAPI(title="Pronuncia Italiana API (Python)")


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"error": str(exc.detail)})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = [{"msg": e.get("msg", "Invalid input"), "path": e.get("loc", [""])[-1]} for e in exc.errors()]
    return JSONResponse(status_code=400, content={"errors": errors})


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_sqlite_schema()


hosts_dir = PUBLIC_DIR / "hosts"
if hosts_dir.exists() and hosts_dir.is_dir():
    app.mount("/hosts", StaticFiles(directory=str(hosts_dir)), name="hosts")

# API routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(dictionary.router)
app.include_router(search.router)
app.include_router(audio.router)
app.include_router(hosts.router)
app.include_router(progress.router)
app.include_router(stories.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": "backend-python"}
