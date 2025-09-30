from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base

engine = create_engine("postgresql+psycopg2://harsh:abc123@localhost:5432/compario")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)  