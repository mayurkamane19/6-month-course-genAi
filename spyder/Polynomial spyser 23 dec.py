import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv(r"C:\Users\mayur\Downloads\emp_sal.csv")

x = dataset.iloc[:, 1:2].values
y = dataset.iloc[:, 2].values

from sklearn.linear_model import LinearRegression

lin_reg = LinearRegression()
lin_reg.fit(x, y)


import matplotlib.pyplot as plt
plt.scatter(x, y, color='red')   
plt.plot(x, lin_reg.predict(x), color='blue')
plt.title('Linear Regression Graph')
plt.xlabel('Position Level')     
plt.ylabel('Salary')
plt.show()

lin_model_pred = lin_reg.predict([[6.5]])
print(lin_model_pred)

from sklearn.preprocessing import PolynomialFeatures


from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


poly_reg = PolynomialFeatures(degree=2)
x_poly = poly_reg.fit_transform(x)


lin_reg_2 = LinearRegression()
lin_reg_2.fit(x_poly, y)

poly_reg = PolynomialFeatures(degree=2)
x_poly = poly_reg.fit_transform(x)

import matplotlib.pyplot as plt

plt.scatter(x, y, color='red')
plt.plot(x, lin_reg.predict(poly_reg.transform(x)), color='blue')

plt.title('Truth or Bluff (Polynomial Regression)')
plt.xlabel('Position Level')
plt.ylabel('Salary')

plt.show()


lin_model_pred = lin_reg.predict([[6.5]])
print(lin_model_pred)

lin_reg_2.fit(x_poly, y)   
poly_model_pred = lin_reg_2.predict(poly_reg.transform([[6.5]]))
print(poly_model_pred)

