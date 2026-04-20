from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    components = Column(Text, nullable=False)  # store as JSON string
    accessibility = Column(Integer, nullable=False)
    steps = Column(Text, nullable=False)
