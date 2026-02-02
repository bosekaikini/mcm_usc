import pandas as pd
import numpy as np
import scipy.optimize as sop
import matplotlib.pyplot as plt

X = np.array([0,1,2,3,4,5,6,7,8,9,10])
Y = np.array([10,8,3,4,6,8,25,9,4,2,1])


def power_model(x, a, b, c):
    with np.errstate(all='ignore'):
        return a * np.power(np.maximum(x, 1e-10), b) + c


def power_derivative(x, a, b, c):
    with np.errstate(all='ignore'):
        return a * b * np.power(np.maximum(x, 1e-10), b - 1)


def fit_power_function(X, Y):
    params, _ = sop.curve_fit(power_model, X, Y, p0=[10, -0.5, 0], maxfev=10000)
    a, b, c = params
    
    y_pred = power_model(X, *params)
    r_squared = 1 - np.sum((Y - y_pred)**2) / np.sum((Y - np.mean(Y))**2)
    
    print(f"Function: y = {a:.4f}*x^{b:.4f} + {c:.4f}")
    print(f"Diff eq:  dy/dx = {a*b:.4f}*x^{b-1:.4f}")
    print(f"R² = {r_squared:.6f}")
    
    return params


def plot_fit(X, Y, params):
    x_smooth = np.linspace(X.min(), X.max(), 200)
    y_fit = power_model(x_smooth, *params)



    dy_dx = power_derivative(x_smooth, *params)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    ax1.scatter(X, Y, color='red', label='Data', s=50)
    ax1.plot(x_smooth, y_fit, color='blue', label='Power Fit', linewidth=2)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_title('Power Function Fit')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(x_smooth, dy_dx, color='green', linewidth=2)
    ax2.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    ax2.set_xlabel('X')
    ax2.set_ylabel('dy/dx')
    ax2.set_title('Derivative (Differential Equation)')
    ax2.grid(True, alpha=0.3)
    plt.show()


params = fit_power_function(X, Y)
plot_fit(X, Y, params)

# Now you can use the fitted function on new data
a, b, c = params
test_x = 5.5
test_y = power_model(test_x, a, b, c)
print(f"  y({test_x}) = {test_y:.4f}")
print(f"  dy/dx({test_x}) = {power_derivative(test_x, a, b, c):.4f}")