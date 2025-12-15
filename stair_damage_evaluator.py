import numpy as np
from scipy.integrate import dblquad
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

X_MIN, X_MAX = 0, 10
Y_MIN, Y_MAX = 0, 5
Z_TOP_PLANE = 7

def z_top(x, y):
    return Z_TOP_PLANE

def z_bottom_surface_analytical(y, x):
    wear_bumpiness = 0.6 * (np.sin(x / X_MAX * 1.5 * np.pi) + np.cos(y / Y_MAX * 1.5 * np.pi))
    height = 6.0 + wear_bumpiness
    return np.clip(height, 0.5, Z_TOP_PLANE - 0.5)

def height_difference_func_simple(y, x):
    return z_top(x, y) - z_bottom_surface_analytical(y, x)

volume_difference, error = dblquad(
    height_difference_func_simple, 
    X_MIN, X_MAX, 
    lambda x: Y_MIN,
    lambda x: Y_MAX 
)

print(f"The continuous volume difference between the planes is: ",volume_difference, "cubic units")

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
x_plot = np.linspace(X_MIN, X_MAX, 50)
y_plot = np.linspace(Y_MIN, Y_MAX, 50)
X_plot, Y_plot = np.meshgrid(x_plot, y_plot)
Z_top_plot = np.full_like(X_plot, Z_TOP_PLANE)
Z_bottom_plot = z_bottom_surface_analytical(Y_plot, X_plot)

ax.plot_surface(X_plot, Y_plot, Z_top_plot, color='skyblue', alpha=0.3)
ax.plot_surface(X_plot, Y_plot, Z_bottom_plot, color='sienna', alpha=0.9)

ax.set_title('Continuous Surface Visualization')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
plt.show()
