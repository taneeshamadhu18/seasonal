# ===============================
# 1. Import Libraries
# ===============================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===============================
# 2. Generate Synthetic Dataset (1000 rows, 5 diseases)
# ===============================
states = ['Assam', 'Arunachal', 'Nagaland', 'Manipur', 'Mizoram', 'Tripura']
diseases = ['Diarrhoea', 'Typhoid', 'Cholera', 'Hepatitis', 'Dengue']
years = [2020, 2021, 2022, 2023]
periods = ['Dec-Feb (Winter)', 'Mar-May (Spring)', 'Jun-Aug (Summer)', 'Sep-Nov (Autumn)']

data = []

np.random.seed(42)

while len(data) < 1000:
    state = np.random.choice(states)
    disease = np.random.choice(diseases)
    year = np.random.choice(years)
    period = np.random.choice(periods)
    
    if state == 'Assam' and period == 'Dec-Feb (Winter)' and disease == 'Typhoid':
        cases = np.random.randint(80, 120)
    elif state == 'Arunachal' and period == 'Mar-May (Spring)' and disease == 'Diarrhoea':
        cases = np.random.randint(70, 110)
    elif state == 'Nagaland' and period == 'Jun-Aug (Summer)' and disease == 'Cholera':
        cases = np.random.randint(60, 100)
    elif state == 'Manipur' and period == 'Sep-Nov (Autumn)' and disease == 'Hepatitis':
        cases = np.random.randint(50, 90)
    elif state == 'Mizoram' and period == 'Mar-May (Spring)' and disease == 'Dengue':
        cases = np.random.randint(40, 80)
    else:
        cases = np.random.randint(10, 50)
    
    data.append([state, disease, year, period, cases])

df = pd.DataFrame(data, columns=['state', 'disease', 'year', 'period', 'cases'])

# ===============================
# 3. Plot Cases per State vs Period for each disease
# ===============================
for disease in diseases:
    plt.figure(figsize=(12,6))
    disease_df = df[df['disease'] == disease]
    
    agg_df = disease_df.groupby(['state', 'period'])['cases'].sum().reset_index()
    pivot_df = agg_df.pivot(index='period', columns='state', values='cases').fillna(0)
    
    pivot_df.plot(kind='bar', stacked=False, figsize=(12,6))
    plt.title(f"{disease} Cases per State Across Periods")
    plt.xlabel("Period")
    plt.ylabel("Number of Cases")
    plt.xticks(rotation=45)
    plt.legend(title="State")
    plt.tight_layout()
    plt.show()

# ===============================
# 4. Generate Conclusion
# ===============================
conclusion = []

for state in states:
    for disease in diseases:
        # Aggregate total cases per period for this state-disease
        subset = df[(df['state'] == state) & (df['disease'] == disease)]
        period_cases = subset.groupby('period')['cases'].sum()
        top_period = period_cases.idxmax()
        max_cases = period_cases.max()
        conclusion.append(f"{state} has the highest {disease} cases in {top_period} with {max_cases} cases.")

# Print the conclusion
print("✅ Summary Conclusion:\n")
for line in conclusion:
    print(line)
