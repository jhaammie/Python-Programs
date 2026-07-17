import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Load the Kaggle dataset
df = pd.read_csv("student_performance.csv")

# 2. View the structure. df = dataframe which resembles a spreadsheet
print(df.head()) # df.head returns the first n rows where the default for n = 5

# 3. Plot the relationship to show students the visual trend
# alpha is the transparency of the colour and can be from 0 to 1
plt.scatter(df['weekly_self_study_hours'], df['total_score'], alpha=0.8, color='grey')
plt.xlabel('Weekly Self Study Hours')
plt.ylabel('Total Score')
# Separate target and features for Simple Linear Regression
plt.title('Study Hours vs. Final Score')
plt.show()

X = df[['weekly_self_study_hours']] # Note the double brackets for a 2D array
y = df['total_score']

# Split into 80% Training and 20% Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and fit the model
simple_model = LinearRegression()
simple_model.fit(X_train, y_train)

# Extract the mathematical coefficients
intercept = simple_model.intercept_
slope = simple_model.coef_[0]

print(f"Intercept (b0): {intercept:.2f}")
print(f"Slope (b1): {slope:.2f}")