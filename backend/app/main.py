from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.routers import scan
from app.database import engine, Base
from app.api.routers.admin import reports
import app.ml.model_loader as model_loader
import app.api.routers.auth as auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)
    print("[startup] Database tables ready.")

    # Pre-load the ML model so the first request isn't slow
    model_loader.load_pipeline()
    print("[startup] ML pipeline loaded.")

    yield  # app is now running and serving requests

    # ── Shutdown ─────────────────────────────────────────────
    print("[shutdown] Cleaning up.")


app = FastAPI(
    title="CyberShield JO",
    description="",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    if len(errors) == 1:
        return JSONResponse(status_code=422, content={"detail": errors[0].get("msg")})
    return JSONResponse(status_code=422, content={"detail": [err.get("msg") for err in errors]})


app.include_router(scan.router)
app.include_router(reports.router)
app.include_router(auth.router, prefix="/auth")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}