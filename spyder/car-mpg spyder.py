import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score

data = pd.read_csv(r"C:\Users\mayur\Downloads\car-mpg.csv")
data.head()

data.head(20)

data.head()

import numpy as np
import pandas as pd

# clean column names
data.columns = data.columns.str.strip().str.lower()
# drop car_name safely
data.drop(columns=['car_name'], errors='ignore', inplace=True)
# encode origin only if present
if 'origin' in data.columns:
    data['origin'] = data['origin'].map({
        1: 'america',
        2: 'europe',
        3: 'asia'
    })
    data = pd.get_dummies(data, columns=['origin'], dtype=int)
# replace missing symbols
data.replace('?', np.nan, inplace=True)

import numpy as np
import pandas as pd

for col in data.columns:
    try:
        data[col] = pd.to_numeric(data[col])
    except (ValueError, TypeError):
        pass  # non-numeric columns stay unchanged

numeric_cols = data.select_dtypes(include=[np.number]).columns
data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].median())


data.head()

data

import pandas as pd
from sklearn.preprocessing import StandardScaler

# Split features & target
x = data.drop('mpg', axis=1)
y = data[['mpg']]

# Scaling
scaler = StandardScaler()

x_s = pd.DataFrame(
    scaler.fit_transform(x),
    columns=x.columns
)

y_s = pd.DataFrame(
    scaler.fit_transform(y),
    columns=y.columns
)

print(x_s.head())
print(y_s.head())


x_s

data.shape

x_train, x_test, y_train,y_test = train_test_split(x_s, y_s, test_size = 0.30, random_state = 1)
x_train.shape

from sklearn.linear_model import LinearRegression

regression_model = LinearRegression()
regression_model.fit(x_train, y_train)

# Print coefficients
for idx, col_name in enumerate(x_train.columns):
    print(
        'The coefficient for {} is {}'.format(
            col_name, regression_model.coef_[0][idx]
        )
    )

# Print intercept
intercept = regression_model.intercept_[0]
print('The intercept is {}'.format(intercept))

ridge_model = Ridge(alpha = 0.3)
ridge_model.fit(x_train, y_train)

print('Ridge model coef:{}'.format(ridge_model.coef_))

lasso_model = Lasso(alpha = 0.1)
lasso_model.fit(x_train, y_train)

print('Lassomodel coef:{}'.format(lasso_model.coef_))

print(regression_model.score(x_train, y_train))
print(regression_model.score(x_test, y_test))
print('*************************')
#Ridge
print(ridge_model.score(x_train, y_train))
print(ridge_model.score(x_test, y_test))
print('*************************')
#Lasso
print(lasso_model.score(x_train, y_train))
print(lasso_model.score(x_test, y_test))

data_train_test = pd.concat([x_train, y_train],axis =1)
data_train_test.head()

import statsmodels.formula.api as smf   # ✅ correct library

ols1 = smf.ols(
    formula='mpg ~ cyl + disp + hp + wt + acc + yr + car_type + origin_america + origin_asia',
    data=data_train_test
).fit()

print(ols1.params)

print(ols1.summary())

mse  = np.mean((regression_model.predict(x_test)-y_test)**2)
# root of mean_sq_error is standard deviation i.e. avg variance between predicted and actual
import math
rmse = math.sqrt(mse)
print('Root Mean Squared Error: {}'.format(rmse))

fig = plt.figure(figsize=(10,8))
sns.residplot(x= x_test['hp'], y= y_test['mpg'], color='green', lowess=True )

fig = plt.figure(figsize=(10,8))
sns.residplot(x= x_test['acc'], y= y_test['mpg'], color='green', lowess=True )

y_pred = regression_model.predict(x_test)
plt.scatter(y_test['mpg'], y_pred)


