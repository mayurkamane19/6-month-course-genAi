import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

dataset = pd.read_csv(r"C:\Users\mayur\Downloads\emp_sal.csv")

x = dataset.iloc[:, 1:2].values
y = dataset.iloc[:, 2].values

from sklearn.svm import SVR

regressor = SVR()
regressor.fit(x, y)

regressor = SVR(kernel="poly", degree=5)
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

from sklearn.neighbors import KNeighborsRegressor
knn_reg = KNeighborsRegressor(n_neighbors=4)
knn_reg.fit(x, y)

from sklearn.neighbors import KNeighborsRegressor

knn_reg = KNeighborsRegressor(n_neighbors=4, weights='distance')
knn_reg.fit(x, y)



y_pred_svr = regressor.predict([[6.5]])
print(y_pred_svr)

