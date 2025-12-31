from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class Cookie(Base):
    __tablename__ = "cookies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String, nullable=False)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    expiration = Column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint('domain', 'name', name='_domain_name_uc'),)
