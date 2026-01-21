import numpy as np
import matplotlib.pyplot as plt

def find_tt_power_curve(cp_mean, w_prime_mean, pan):
    t = np.linspace(1, 3600, 1000)
    
    wp_j = w_prime_mean * 1000
    tau = wp_j / pan
    p = cp_mean + pan / (1 + (t / tau))
    power_curve_data = {'time_seconds': t, 'power_watts': p}
    return power_curve_data
    