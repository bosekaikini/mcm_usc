import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
from scipy.optimize import minimize
from scipy.integrate import cumulative_trapezoid

MASS_SYS = 72.6 + 8.0
G = 9.81
RHO = 1.225
CDA = 0.276
CRR = 0.004

def solve_velocity(power, slope):
    alpha = np.arctan(slope)
    a_coeff = 0.5 * CDA * RHO
    b_coeff = 0
    c_coeff = MASS_SYS * G * (np.sin(alpha) + CRR * np.cos(alpha))
    d_coeff = -power
    
    roots = np.roots([a_coeff, b_coeff, c_coeff, d_coeff])
    real_roots = roots[np.isreal(roots)].real
    return real_roots[real_roots > 0][0]

def check_energy_constraint(power_history, time_history, cp_mean, cp_sd, w_prime_mean):
    if len(power_history) < 2:
        return True
    total_energy_used = cumulative_trapezoid(power_history, time_history, initial=0)[-1]
    t_star = time_history[-1]
    max_allowable_energy = (cp_mean + cp_sd) * t_star + (w_prime_mean * 1000)
    return total_energy_used <= max_allowable_energy

def calculate_next_optimal_power_value(cp_mean, cp_sd, w_prime_mean, pan, track):
    # Initialize with 0 to keep lengths aligned for integration
    powers = [0.0] 
    times = [0.0]
    total_time = 0.0
    
    for point in track.points:
        # 1. Local Greedy Choice
        target_p = cp_mean + (pan if point.slope > 0 else 0)
        
        # 2. Physics: Solve for velocity
        v = solve_velocity(target_p, point.slope)
        dt = point.segment_length / v
        
        # 3. Build temporary lists for the constraint check
        temp_p = powers + [target_p]
        temp_t = times + [total_time + dt]
        
        # 4. Check Energy Boundary
        if not check_energy_constraint(temp_p, temp_t, cp_mean, cp_sd, w_prime_mean):
            target_p = cp_mean
            v = solve_velocity(target_p, point.slope)
            dt = point.segment_length / v
        
        # Update actual histories
        powers.append(target_p)
        total_time += dt
        times.append(total_time)
        
    # Return slices that ignore the initial [0.0] padding to match track points
    return {
        "powers": np.array(powers[1:]), 
        "times": np.array(times[1:])
    }

def get_optimal_power_function(results, track):
    distances = np.cumsum([p.segment_length for p in track.points])
    powers = results['powers']
    
    power_function = scipy.interpolate.interp1d(
        distances, 
        powers, 
        kind='linear', 
        fill_value="extrapolate"
    )
    return power_function

def plot_optimal_power_function(power_function, total_length):
    distances = np.linspace(0, total_length, 1000)
    powers = power_function(distances)
    
    plt.figure(figsize=(12, 6))
    plt.plot(distances, powers, color='firebrick', label='Deterministic Power P(x)')
    plt.fill_between(distances, 395.3, powers, where=(powers > 395.3), color='red', alpha=0.3, label='W\' Expenditure')
    plt.xlabel('Track Distance (m)')
    plt.ylabel('Power (Watts)')
    plt.title('Optimal Pacing Strategy: Time Trial Specialist')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
