import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv(r"C:\Users\mayur\Downloads\train_test_split_evaluation_dataset.csv")

x = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=0
)

from sklearn.linear_model import LinearRegression
model = LinearRegression()

model.fit(x_train, y_train)

y_pred = model.predict(x_test)

print("Model trained successfully ✅")

plt.scatter(x_test['Hours_Studied'], y_test, color='red')

sleep_mean = x_train['Sleep_Hours'].mean()

x_line = np.linspace(
    x_train['Hours_Studied'].min(),
    x_train['Hours_Studied'].max(),
    100
)

X_line = pd.DataFrame({
    'Hours_Studied': x_line,
    'Sleep_Hours': sleep_mean
})

y_line = model.predict(X_line)

plt.plot(x_line, y_line, color='blue')

plt.xlabel('Hours_Studied')
plt.ylabel('Performance_Score')
plt.title('Performance_Score vs Hours_Studied')
plt.show()

m_slope = model.coef_
print("Slope (m):", m_slope)

c_intercept = model.intercept_
print("Intercept (c):", c_intercept)

y_12 = m_slope*12+c_intercept
print(y_12)

y_20= m_slope*20+c_intercept
print(y_20)

bias_score = model.score(x_train, y_train)
print("Training Score (Bias):", bias_score)

variance_score = model.score(x_test, y_test)
print("Testing Score (Variance):", variance_score)