import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

def plot_tt_power_curve(cp_mean, cp_sd, w_prime_mean, w_prime_sd, pan):
    t = np.linspace(1, 3600, 1000)
    
    wp_j = w_prime_mean * 1000
    wp_sd_j = w_prime_sd * 1000
    tau = wp_j / pan
    
    p_mean = cp_mean + pan / (1 + (t / tau))
    
    tau_high = (wp_j + wp_sd_j) / pan
    tau_low = (wp_j - wp_sd_j) / pan
    p_high = (cp_mean + cp_sd) + pan / (1 + (t / tau_high))
    p_low = (cp_mean - cp_sd) + pan / (1 + (t / tau_low))
    
    plt.plot(t, p_mean, color='blue', label='Mean Time Trialist', linewidth=2)
    plt.fill_between(t, p_low, p_high, color='blue', alpha=0.2, label='Standard Deviation')
    
    plt.xscale('log')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Power (Watts)')
    plt.title('Power-Duration Curve: Time Trial Specialist')
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend()
    plt.savefig('tt_power_profile.png')

plot_tt_power_curve(cp_mean=395.3, cp_sd=31.8, w_prime_mean=22.0, w_prime_sd=2.7, pan=600)