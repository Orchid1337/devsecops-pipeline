from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, items, users

app = FastAPI(
    title="DevSecOps Demo API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Lock down CORS - only our frontend domain gets through
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(items.router)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "DevSecOps Demo API", "docs": "/docs"}
