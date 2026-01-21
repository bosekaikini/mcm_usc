import numpy as np
import matplotlib.pyplot as plt

def plot_tt_power_curve(cp_mean, w_prime_mean, pan):
    t = np.linspace(1, 3600, 1000)
    
    wp_j = w_prime_mean * 1000
    tau = wp_j / pan
    
    p = cp_mean + pan / (1 + (t / tau))
    
    plt.plot(t, p, color='blue', label='Mean Time Trialist', linewidth=2)
    plt.xscale('log')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Power (Watts)')
    plt.title('Power Curve: Time Trial Specialist')
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend()
    plt.savefig('2022_A/tt_power_curve.png')
    vals= {'time_seconds': t, 'power_watts': p}
    return vals

vals=plot_tt_power_curve(cp_mean=395.3, w_prime_mean=22.0, pan=600)
print(vals)