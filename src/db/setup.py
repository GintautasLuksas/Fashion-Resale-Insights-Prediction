"""
Database setup for Fashion Resale project.
Creates the main table if it does not exist.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base

load_dotenv()

Base = declarative_base()

class FashionResale(Base):
    __tablename__ = "fashion_resale"

    product_id = Column(String, primary_key=True, index=True)
    product_type = Column(String, nullable=True)
    brand_name = Column(String, nullable=True)
    product_gender_target = Column(String, nullable=True)
    product_condition = Column(String, nullable=True)
    product_material = Column(String, nullable=True)
    product_color = Column(String, nullable=True)
    price_usd = Column(Float, nullable=True)
    price_log = Column(Float, nullable=True)
    sold = Column(Boolean, nullable=True)
    seller_country = Column(String, nullable=True)
    seller_products_sold = Column(Integer, nullable=True)
    seller_pass_rate = Column(Float, nullable=True)
    brand_encoded = Column(Integer, nullable=True)
    condition_encoded = Column(Integer, nullable=True)
    gender_encoded = Column(Integer, nullable=True)

def create_db_and_tables():
    """
    Create database engine and tables if they don't exist.
    Reads connection info from environment variables.
    """
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")

    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

    try:
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        print("✅ Tables created or already exist.")
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")

if __name__ == "__main__":
    create_db_and_tables()
