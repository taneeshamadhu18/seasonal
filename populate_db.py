from db import engine, disease_table
import pandas as pd
from app import generate_dataset  # your synthetic dataset function

df = generate_dataset()

with engine.connect() as conn:
    for _, row in df.iterrows():
        conn.execute(disease_table.insert().values(
            state=row['state'],
            disease=row['disease'],
            year=row['year'],
            period=row['period'],
            cases=row['cases']
        ))
    conn.commit()

print("✅ Database populated with initial data")
