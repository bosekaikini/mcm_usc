import numpy as np
from scipy.integrate import dblquad
from scipy.interpolate import RectBivariateSpline
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def evaluate_stair_damage(X, Y, Z_worn, HEIGHT):
    # trapezoid rule
    dx = np.abs(X[0, 1] - X[0, 0])
    dy = np.abs(Y[1, 0] - Y[0, 0])
    height_diff = HEIGHT - Z_worn

    volume_difference = np.trapezoid(np.trapezoid(height_diff, dx=dx, axis=1), dx=dy)
    
    return volume_difference


# Example standalone usage with analytical surface
if __name__ == "__main__":
    X_MIN, X_MAX = 0, 10
    Y_MIN, Y_MAX = 0, 5
    Z_TOP_PLANE = 7
    
    def z_bottom_surface_analytical(y, x):
        wear_bumpiness = 0.6 * (np.sin(x / X_MAX * 1.5 * np.pi) + np.cos(y / Y_MAX * 1.5 * np.pi))
        height = 6.0 + wear_bumpiness
        return np.clip(height, 0.5, Z_TOP_PLANE - 0.5)
    
    x_plot = np.linspace(X_MIN, X_MAX, 50)
    y_plot = np.linspace(Y_MIN, Y_MAX, 50)
    X_plot, Y_plot = np.meshgrid(x_plot, y_plot)
    Z_bottom_plot = z_bottom_surface_analytical(Y_plot, X_plot)
    
    volume_diff = evaluate_stair_damage(X_plot, Y_plot, Z_bottom_plot, Z_TOP_PLANE)
    
    print(f"The continuous volume difference between the planes is: {volume_diff} cubic units")