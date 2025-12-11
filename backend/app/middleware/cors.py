"""Custom CORS middleware."""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import os


class SimpleCORSMiddleware(BaseHTTPMiddleware):
    """Simple CORS middleware that allows localhost and production frontend."""

    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin", "")
        frontend_url = os.getenv("FRONTEND_URL", "")

        # Check if origin is allowed (localhost, 127.0.0.1, or production frontend, or Vercel preview)
        is_allowed = (
            origin.startswith("http://localhost") or
            origin.startswith("https://localhost") or
            origin.startswith("http://127.0.0.1") or
            origin.startswith("https://127.0.0.1") or
            origin == frontend_url or
            ".vercel.app" in origin  # Allow all Vercel preview deployments
        )

        # Handle preflight requests
        if request.method == "OPTIONS":
            if is_allowed:
                return Response(
                    status_code=200,
                    headers={
                        "Access-Control-Allow-Origin": origin,
                        "Access-Control-Allow-Methods": "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Credentials": "true",
                        "Access-Control-Max-Age": "600",
                    },
                )
            else:
                return Response(status_code=403, content="Origin not allowed")

        # Handle actual requests
        response = await call_next(request)

        if is_allowed:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Expose-Headers"] = "*"

        return response
