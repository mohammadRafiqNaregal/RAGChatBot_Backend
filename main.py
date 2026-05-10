# Express:  const express = require('express')
# Express:  const userRouter = require('./routes/userRoutes')
import logging
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from data.init_db import init_db
from routers import auth_router
from routers import user_router

# Express:  const app = express()
app = FastAPI(
    title="User Management API",
    version="1.0.0",
)

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

request_logger = logging.getLogger("request_logger")
if not request_logger.handlers:
    request_logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_dir / "requests.log")
    file_handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
    request_logger.addHandler(file_handler)
request_logger.propagate = False


@app.on_event("startup")
def on_startup() -> None:
    init_db()

origins = [
    "http://localhost:5173",  # Vite frontend
    "http://localhost:3000",  # Next.js frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or ["*"] for quick testing
    allow_credentials=True,       # cookies/auth headers
    allow_methods=["*"],          # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],          # Authorization, Content-Type, etc.
)


# Express: app.use((req, res, next) => { ...; next() })
@app.middleware("http")
async def log_and_time_requests(request: Request, call_next):
    started_at = time.perf_counter()
    body_bytes = await request.body()
    body_text = body_bytes.decode("utf-8", errors="replace") if body_bytes else ""

    async def receive():
        return {"type": "http.request", "body": body_bytes, "more_body": False}

    request = Request(request.scope, receive)
    request_logger.info(
        "%s %s | payload=%s",
        request.method,
        request.url.path,
        body_text,
    )

    response = await call_next(request)

    duration = time.perf_counter() - started_at
    response.headers["X-Process-Time"] = f"{duration:.6f}"
    return response

# Express:  app.use('/users', userRouter)
app.include_router(auth_router.router)  
app.include_router(user_router.router)


# Express:  app.get('/', (req, res) => res.json({ message: '...' }))
@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to User Management API", "docs": "/docs"}


# Express:  app.listen(8000, () => console.log('Server running...'))
# FastAPI:  run with →  uvicorn main:app --reload
