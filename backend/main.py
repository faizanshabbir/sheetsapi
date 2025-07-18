from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import sheets, dynamic, dynamic_field
from app.db.init_db import init_db

app = FastAPI(
    title="Sheets API Generator",
    description="Generate APIs from Google Sheets",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(sheets.router, prefix="/api/v1")
app.include_router(dynamic.router, prefix="/api/v1")
app.include_router(dynamic_field.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 