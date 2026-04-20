import json
from sqlalchemy.orm import Session
from app.models import Package

def get_packages(db: Session):
    return db.query(Package).all()

def get_package(db: Session, package_id: int):
    return db.query(Package).filter(Package.id == package_id).first()

def create_package(db: Session, data):
    package = Package(
        name=data.name,
        components=json.dumps(data.components),
        accessibility=data.accessibility,
        steps=json.dumps(data.steps)
    )
    db.add(package)
    db.commit()
    db.refresh(package)
    return package