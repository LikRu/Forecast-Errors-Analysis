import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV file, specifying column names
df = pd.read_csv("forecast_history.csv", header=None, names=['Year', 'Median house price', 'Westpac: 4 year forecast', 'Joe Bloggs: 2 year forecast', 'Harry Spent: 5 year forecast'])

# Correct specific values before replacing symbols
df.loc[df['Joe Bloggs: 2 year forecast'] == 'I5%', 'Joe Bloggs: 2 year forecast'] = '15%'
df['Joe Bloggs: 2 year forecast'] = df['Joe Bloggs: 2 year forecast'].replace({'%': '', '$': ''}, regex=True).astype(float) / 100

# Replace symbols and incorrect values for other columns
df['Westpac: 4 year forecast'] = df['Westpac: 4 year forecast'].replace({'%': '', 'O': '0', '$': ''}, regex=True).astype(float) / 100
df['Harry Spent: 5 year forecast'] = df['Harry Spent: 5 year forecast'].replace({'%': '', '$': ''}, regex=True).astype(float) / 100

# Correct the median house price for the year 2023 and 2024
df.loc[df['Year'] == 2023, 'Median house price'] = 730000
df.loc[df['Year'] == 2024, 'Median house price'] = 760000

# Handle missing values by removing rows with any missing values
df = df.dropna()

# Handle extreme outliers (e.g., 1500%)
df = df[df['Joe Bloggs: 2 year forecast'] < 10]  # Remove extreme values

# Summary of results
summary = {
    'Forecaster': ['Westpac', 'Joe Bloggs', 'Harry Spent'],
    'Average_Error': [
        df['Westpac: 4 year forecast'].mean(),
        df['Joe Bloggs: 2 year forecast'].mean(),
        df['Harry Spent: 5 year forecast'].mean()
    ],
    'Median_Error': [
        df['Westpac: 4 year forecast'].median(),
        df['Joe Bloggs: 2 year forecast'].median(),
        df['Harry Spent: 5 year forecast'].median()
    ],
    'Max_Error': [
        df['Westpac: 4 year forecast'].max(),
        df['Joe Bloggs: 2 year forecast'].max(),
        df['Harry Spent: 5 year forecast'].max()
    ],
    'Min_Error': [
        df['Westpac: 4 year forecast'].min(),
        df['Joe Bloggs: 2 year forecast'].min(),
        df['Harry Spent: 5 year forecast'].min()
    ],
    'Standard_Deviation': [
        df['Westpac: 4 year forecast'].std(),
        df['Joe Bloggs: 2 year forecast'].std(),
        df['Harry Spent: 5 year forecast'].std()
    ]
}

summary_df = pd.DataFrame(summary)

# Print results
print("Forecast Accuracy Summary:")
print(summary_df)

# Plotting the errors
plt.figure(figsize=(12, 8))
plt.plot(df['Year'], df['Westpac: 4 year forecast'], marker='o', label='Westpac Forecast Error')
plt.plot(df['Year'], df['Joe Bloggs: 2 year forecast'], marker='o', label='Joe Bloggs Forecast Error')
plt.plot(df['Year'], df['Harry Spent: 5 year forecast'], marker='o', label='Harry Spent Forecast Error')
plt.xlabel('Year')
plt.ylabel('Forecast Error (%)')
plt.title('Forecast Error Comparison')
plt.legend()
plt.grid(True)
plt.savefig('forecast_error_comparison.png')
plt.show()

# Save summary to CSV
summary_df.to_csv('forecast_accuracy_summary.csv', index=False)
