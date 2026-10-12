import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Small dataset with a bit of noise
np.random.seed(0)
X = np.linspace(0, 10, 15).reshape(-1, 1)
y = 2 * X.flatten() + np.random.normal(0, 3, 15)  # true pattern: y ≈ 2x, plus noise

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

# Deliberately overfit: degree-12 polynomial on only 10 training points
poly = PolynomialFeatures(degree=12)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

model = LinearRegression()
model.fit(X_train_poly, y_train)

print("Train R² score:", model.score(X_train_poly, y_train))
print("Test R² score:", model.score(X_test_poly, y_test))