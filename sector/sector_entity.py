from sqlalchemy import Column, BigInteger, String, TIMESTAMP
from common.database import Base

class Sector(Base):
    __tablename__ = "sectors"

    id = Column(BigInteger, primary_key=True)
    sector_key = Column(String(50), unique=True, nullable=False)
    sector_display = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP)
