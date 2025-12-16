import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats


dataset = pd.read_csv(
    r"C:\Users\mayur\Downloads\simple_linear_regression_dataset.csv"
)

print("\nDataset Preview:")
print(dataset.head())

print("\nDataset Columns:")
print(dataset.columns)


X = dataset.iloc[:, :-1]     
y = dataset.iloc[:, -1]      

feature_name = X.columns[0]
target_name = y.name

print(f"\nFeature Used : {feature_name}")
print(f"Target Used  : {target_name}")

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

comparison = pd.DataFrame({
    f"Actual {target_name}": y_test.values,
    f"Predicted {target_name}": y_pred
})

print("\nPrediction Comparison:")
print(comparison)

if X.shape[1] == 1:
    plt.scatter(X_test, y_test)
    plt.plot(X_train, model.predict(X_train))
    plt.xlabel(feature_name)
    plt.ylabel(target_name)
    plt.title(f"{target_name} vs {feature_name}")
    plt.show()

m = model.coef_[0]
c = model.intercept_

print("\nRegression Equation:")
print(f"{target_name} = {m:.4f} * {feature_name} + {c:.4f}")

example_value = X.iloc[:, 0].mean()
future_prediction = m * example_value + c

print(
    f"Prediction for {feature_name} = {example_value:.2f} : {future_prediction}"
)

bias_training = model.score(X_train, y_train)
variance_testing = model.score(X_test, y_test)

print("\nModel Evaluation:")
print("Training Score (Bias):", bias_training)
print("Testing Score (Variance):", variance_testing)

print("\nDescriptive Statistics:")
print("Mean:\n", dataset.mean())
print("\nMedian:\n", dataset.median())
print("\nVariance:\n", dataset.var())
print("\nStandard Deviation:\n", dataset.std())

print("\nCoefficient of Variation:")
print(stats.variation(dataset, axis=0))

print("\nCorrelation Matrix:")
print(dataset.corr())

print("\nSkewness:")
print(dataset.skew())

print("\nStandard Error of Mean:")
print(dataset.sem())

z_scores = dataset.apply(stats.zscore)
print("\nZ-Scores:")
print(z_scores)

y_pred_full = model.predict(X)
y_mean = np.mean(y)

SSR = np.sum((y_pred_full - y_mean) ** 2)
SSE = np.sum((y - y_pred_full) ** 2)
SST = np.sum((y - y_mean) ** 2)

r_square = SSR / SST

print("\nANOVA Results:")
print("SSR:", SSR)
print("SSE:", SSE)
print("SST:", SST)
print("R² Score:", r_square)

print("\nFINAL SUMMARY")
print("Bias (Training Score):", bias_training)
print("Variance (Testing Score):", variance_testing)
print("R² Score:", r_square)
