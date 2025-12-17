import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load dataset
dataset = pd.read_csv(
    r"C:\Users\mayur\Downloads\17th - mlr\17th - mlr\MLR\House_data.csv"
)

# Check nulls & datatypes
print(dataset.isnull().any())
print(dataset.dtypes)

# Independent (X) & Dependent (y)
X = dataset.iloc[:, 1].values.reshape(-1, 1)  # FIX: X + 2D
y = dataset.iloc[:, 0].values                 # target

# Train-test split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=1/3,
    random_state=0
)

print("X_train shape:", X_train.shape)
print("X_test shape :", X_test.shape)

# Convert date string to datetime
dataset['date'] = pd.to_datetime(dataset['date'])

# Convert datetime to numeric (timestamp)
dataset['date'] = dataset['date'].astype('int64')

# Now split
X = dataset.iloc[:, 1:].values
y = dataset.iloc[:, 0].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=1/3, random_state=0
)

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# ================= BACKWARD ELIMINATION (ONE CELL) =================

import numpy as np
import pandas as pd
import statsmodels.api as sm

# Load dataset
dataset = pd.read_csv(
    r"C:\Users\mayur\Downloads\17th - mlr\17th - mlr\MLR\House_data.csv"
)

# Keep only numeric columns (VERY IMPORTANT)
dataset = dataset.select_dtypes(include=[np.number])

# Define X (features) and y (target)
X = dataset.iloc[:, 1:].values   # independent variables
y = dataset.iloc[:, 0].values    # dependent variable

# Add constant (intercept)
X = sm.add_constant(X)

# Backward Elimination function
def backwardElimination(X, y, SL=0.05):
    X_opt = X.copy()
    while True:
        model = sm.OLS(y, X_opt).fit()
        pvalues = model.pvalues
        max_pval = pvalues.max()
        if max_pval > SL:
            X_opt = np.delete(X_opt, pvalues.argmax(), axis=1)
        else:
            break
    print(model.summary())
    return X_opt

# Run Backward Elimination
SL = 0.05
X_Modeled = backwardElimination(X, y, SL)

print("Final Selected Features Shape:", X_Modeled.shape)

