import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv(r"C:\Users\mayur\Downloads\Investment.csv")

x = dataset.iloc[:, :-1]
y = dataset.iloc[:, 4]

x = pd.get_dummies(x, dtype=int)

from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=0)

from sklearn.linear_model import LinearRegression 
regressor = LinearRegression()
regressor.fit(xtrain, ytrain)

#Predicting
ypred = regressor.predict(xtest)

m = regressor.coef_
print(m)

c = regressor.intercept_
print(c)

x = np.append(arr=np.full((50,1), 42467).astype(int), values=x, axis=1)

import statsmodels.api as sm

# Step 1: Add constant (important for intercept)
x = sm.add_constant(x)

# Step 2: Select columns
x_opt = x[:, [0, 1, 2, 3, 4, 5]]

# Step 3: Fit OLS model
regressor_OLS = sm.OLS(endog=y, exog=x_opt).fit()

# Step 4: Print summary
print(regressor_OLS.summary())

import statsmodels.api as sm

# Step 1: Add constant (important for intercept)
x = sm.add_constant(x)

# Step 2: Select columns
x_opt = x[:, [0, 1, 2, 3, 5]]

# Step 3: Fit OLS model
regressor_OLS = sm.OLS(endog=y, exog=x_opt).fit()

# Step 4: Print summary
print(regressor_OLS.summary())

import statsmodels.api as sm

# Step 1: Add constant (important for intercept)
x = sm.add_constant(x)

# Step 2: Select columns
x_opt = x[:, [0, 1, 2, 3]]

# Step 3: Fit OLS model
regressor_OLS = sm.OLS(endog=y, exog=x_opt).fit()

# Step 4: Print summary
print(regressor_OLS.summary())

import statsmodels.api as sm

# Step 1: Add constant (important for intercept)
x = sm.add_constant(x)

# Step 2: Select columns
x_opt = x[:, [0, 1]]

# Step 3: Fit OLS model
regressor_OLS = sm.OLS(endog=y, exog=x_opt).fit()

# Step 4: Print summary
print(regressor_OLS.summary())



from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Split data
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=0
)

# Create model
model = LinearRegression()

# Train model
model.fit(x_train, y_train)

# Now score will work
bias_score = model.score(x_train, y_train)
print("Training R² Score:", bias_score)

variance_score = model.score(x_test, y_test)
print("Testing R² Score :", variance_score)
