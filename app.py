# ===============================
# FastAPI with PostgreSQL
# ===============================
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from db import SessionLocal
from sqlalchemy import text
import matplotlib.pyplot as plt
import io, base64

app = FastAPI(title="Disease Cases Analysis API")

# ===============================
# 1. Utility: Fetch Data from DB
# ===============================
def fetch_dataset():
    db = SessionLocal()
    result = db.execute(text("SELECT * FROM disease_cases")).fetchall()
    db.close()
    return [dict(row._mapping) for row in result]


# ===============================
# 2. API Endpoints
# ===============================

@app.get("/")
def root():
    return {"message": "Welcome to Disease Cases Analysis API (DB Connected)!"}


@app.get("/dataset")
def get_dataset():
    """Return all rows from the DB"""
    data = fetch_dataset()
    return JSONResponse(content=data)


@app.get("/plot/{disease}")
def get_plot(disease: str):
    """Return bar chart for a given disease (base64 encoded image)"""
    data = fetch_dataset()
    if not data:
        return {"error": "No data available"}

    import pandas as pd
    df = pd.DataFrame(data)
    disease_df = df[df['disease'] == disease]

    if disease_df.empty:
        return {"error": f"No data found for {disease}"}

    agg_df = disease_df.groupby(['state', 'period'])['cases'].sum().reset_index()
    pivot_df = agg_df.pivot(index='period', columns='state', values='cases').fillna(0)

    # Plot
    plt.figure(figsize=(10,6))
    pivot_df.plot(kind='bar', figsize=(10,6))
    plt.title(f"{disease} Cases per State Across Periods")
    plt.xlabel("Period")
    plt.ylabel("Cases")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return {"disease": disease, "plot_base64": encoded}


@app.get("/conclusion")
def get_conclusion():
    """Return text summary for all states & diseases"""
    data = fetch_dataset()
    if not data:
        return {"error": "No data available"}

    import pandas as pd
    df = pd.DataFrame(data)

    states = df['state'].unique()
    diseases = df['disease'].unique()

    conclusion = []
    for state in states:
        for disease in diseases:
            subset = df[(df['state'] == state) & (df['disease'] == disease)]
            if subset.empty:
                continue
            period_cases = subset.groupby('period')['cases'].sum()
            top_period = period_cases.idxmax()
            max_cases = int(period_cases.max())
            conclusion.append(f"{state} has the highest {disease} cases in {top_period} with {max_cases} cases.")

    return {"conclusion": conclusion}
