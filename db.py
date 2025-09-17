import os
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://seasonal_pred_user:4lJWv1Z8zsz2wbqdPlt3pPRZ7BJNbjcB@dpg-d35a40e3jp1c73esth50-a.oregon-postgres.render.com/seasonal_pred")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()

disease_table = Table(
    'disease_cases', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('state', String),
    Column('disease', String),
    Column('year', Integer),
    Column('period', String),
    Column('cases', Integer)
)

metadata.create_all(engine)
