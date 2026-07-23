# SQLAlchemy PostgreSQL models & ingestion
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Bank(Base):
    __tablename__ = 'banks'
    
    bank_id = Column(Integer, primary_key=True, autoincrement=True)
    bank_name = Column(String(100), nullable=False, unique=True)
    app_id = Column(String(150), nullable=False)
    reviews = relationship("Review", back_populates="bank")

class Review(Base):
    __tablename__ = 'reviews'
    
    review_id = Column(String(255), primary_key=True)
    bank_id = Column(Integer, ForeignKey('banks.bank_id'), nullable=False)
    review_text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    review_date = Column(Date, nullable=False)
    sentiment_label = Column(String(50))
    sentiment_score = Column(Float)
    identified_theme = Column(String(100))
    source = Column(String(50), default="Google Play")
    
    bank = relationship("Bank", back_populates="reviews")