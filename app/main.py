from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import crud
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SilverLink Care Package API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PackageCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    components: List[str] = Field(..., min_items=1)
    accessibility: int = Field(..., ge=1, le=10)
    steps: List[str] = Field(..., min_items=1)


class PackageResponse(BaseModel):
    id: int
    name: str
    components: List[str]
    accessibility: int
    steps: List[str]


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/packages", response_model=List[PackageResponse])
def get_packages(db: Session = Depends(get_db)):
    """Retrieve all care packages"""
    packages = crud.get_packages(db)
    return [
        {
            "id": p.id,
            "name": p.name,
            "components": json.loads(p.components),
            "accessibility": p.accessibility,
            "steps": json.loads(p.steps),
        }
        for p in packages
    ]


@app.get("/packages/{package_id}", response_model=PackageResponse)
def get_package(package_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific package by ID"""
    if package_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid package ID")

    package = crud.get_package(db, package_id)

    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    return {
        "id": package.id,
        "name": package.name,
        "components": json.loads(package.components),
        "accessibility": package.accessibility,
        "steps": json.loads(package.steps),
    }


@app.post("/packages", response_model=PackageResponse, status_code=201)
def create_package(data: PackageCreate, db: Session = Depends(get_db)):
    """Create a new care package"""
    package = crud.create_package(db, data)

    return {
        "id": package.id,
        "name": package.name,
        "components": json.loads(package.components),
        "accessibility": package.accessibility,
        "steps": json.loads(package.steps),
    }