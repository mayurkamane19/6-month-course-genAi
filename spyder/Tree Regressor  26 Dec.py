import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

dataset = pd.read_csv(r"C:\Users\mayur\Downloads\emp_sal.csv")

x = dataset.iloc[:, 1:2].values
y = dataset.iloc[:, 2].values

from sklearn.svm import SVR

regressor = SVR()
regressor.fit(x, y)

from sklearn.svm import SVR
regressor = SVR(kernel="poly", degree=4, gamma="auto", C=5.0)
regressor.fit(x, y)

regressor = SVR(kernel="linear", degree=5)
regressor.fit(x, y)

from sklearn.neighbors import KNeighborsRegressor
knn_reg = KNeighborsRegressor()
knn_reg.fit(x, y)

y_pred_knn = knn_reg.predict([[6.5]])
print(y_pred_knn)


from sklearn.tree import DecisionTreeRegressor

dt_reg = DecisionTreeRegressor(random_state=0)
dt_reg.fit(x, y)

dt_pred = dt_reg.predict([[6.5]])
print(dt_pred)

from sklearn.tree import DecisionTreeRegressor

dt_reg = DecisionTreeRegressor(criterion='absolute_error',max_depth=3)
dt_reg.fit(x, y)

dt_reg = DecisionTreeRegressor(criterion='absolute_error',max_depth=5)
dt_reg.fit(x, y)

dt_reg = DecisionTreeRegressor(criterion='poisson',max_depth=3,random_state=0)
dt_reg.fit(x, y)

dt_reg = DecisionTreeRegressor(criterion='poisson',max_depth=5,random_state=0)
dt_reg.fit(x, y)


dt_pred = dt_reg.predict([[6.5]])
print(dt_pred)



# random forest Algorithm
from sklearn.ensemble import RandomForestRegressor
rf_reg =RandomForestRegressor()
rf_reg.fit(x, y)

rf_pred = rf_reg.predict([[6.5]])
print(rf_pred)

