"""Main FastAPI application for BookClub Platform."""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging
from .config import get_settings
from .database import engine, Base
from .routers import auth, users, groups, books, comments, progress
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="BookClub Platform API",
    description="Backend API for the BookClub reading platform with Google OAuth, group management, and comment visibility based on reading progress.",
    version="1.0.0",
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url="/redoc" if settings.environment == "development" else None,
)

# Configure CORS - Using FastAPI's built-in middleware
logger.info(f"Setting up CORS middleware for environment: {settings.environment}")

# Build explicit allowlist from env (supports comma-separated) + common local dev hosts
def expand_origin(origin: str) -> list[str]:
    """Normalize origin strings; if scheme missing, include both https/http variants."""
    cleaned = origin.strip().rstrip("/")
    if not cleaned:
        return []
    if cleaned.startswith(("http://", "https://")):
        return [cleaned]
    return [f"https://{cleaned}", f"http://{cleaned}"]


env_origins: list[str] = []
for raw_origin in settings.frontend_url.split(","):
    env_origins.extend(expand_origin(raw_origin))

allowed_origins = {
    *env_origins,
    "http://localhost:5173",
    "https://localhost:5173",
    "http://localhost:3000",
    "https://localhost:3000",
}

allowlist = [origin for origin in allowed_origins if origin]
logger.info(f"CORS allowed origins: {allowlist}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowlist,
    allow_origin_regex=".*",  # fallback to ensure header on any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS middleware added successfully")


# Final safety net: ensure CORS headers are present on every response, including errors
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    origin = request.headers.get("origin", "")

    # Preflight handling (covers cases where upstream middleware might not run)
    if request.method == "OPTIONS":
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={},
            headers={
                "Access-Control-Allow-Origin": origin or "*",
                "Access-Control-Allow-Methods": "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
                "Access-Control-Allow-Headers": request.headers.get("Access-Control-Request-Headers", "*"),
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "600",
            },
        )

    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = origin or "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Expose-Headers"] = "*"
    response.headers.setdefault("Access-Control-Allow-Methods", "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT")
    response.headers.setdefault("Access-Control-Allow-Headers", "Content-Type, Authorization, *")
    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed messages."""
    logger.warning(f"Validation error on {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "message": "Validation error in request data"
        },
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors."""
    logger.error(f"Database error on {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "A database error occurred",
            "message": "Internal server error"
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    logger.error(f"Unhandled error on {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred",
            "message": "Internal server error"
        },
    )


# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(books.router)
app.include_router(comments.router)
app.include_router(progress.router)


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - health check."""
    return {
        "status": "healthy",
        "service": "BookClub Platform API",
        "version": "1.0.0",
        "environment": settings.environment
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    try:
        # Test database connection
        from .database import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = "unhealthy"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status,
        "environment": settings.environment
    }


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("BookClub Platform API starting up...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Frontend URL: {settings.frontend_url}")
    logger.info("Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("BookClub Platform API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development"
    )
