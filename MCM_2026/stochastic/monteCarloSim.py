import numpy as np
import matplotlib.pyplot as plt
import stochastic_full as sf


num_simulations = 100
N = 50000  # number of time steps
T = sf.totalBatteryLife * 1.2
dt = T / N
timeInHours = np.linspace(0, T, N)

def run_sim(initial_soc, capacity_health, power_params):
    soc_path = np.zeros(N)
    soc_path[0] = initial_soc
    
    for i in range(1, N):
        soc_new, _ = sf.rk4_step_soc(soc_path[i-1], timeInHours[i-1], dt)
        soc_path[i] = soc_new
        if soc_new <= 0:  # Stop simulation when SOC reaches 0
            soc_path[i:] = 0
            break
    
    return soc_path

def run_monte_carlo(num_simulations, initial_soc, capacity_health, power_params):
    """Run multiple Monte Carlo simulations"""
    paths = np.zeros((num_simulations, N))
    for k in range(num_simulations):
        paths[k, :] = run_sim(initial_soc, capacity_health, power_params)
    return paths

def plot_monte_carlo_results(paths):
    """Plot all simulated SOC paths"""
    plt.figure(figsize=(12, 6))
    # Plot each simulation path with low alpha for transparency
    for i in range(paths.shape[0]):
        plt.plot(timeInHours, paths[i], alpha=0.05, color='orange')
    
    plt.title("Monte Carlo Simulation: SOC Diffusion Paths")
    plt.xlabel("Time (hours)")
    plt.ylabel("State of Charge (%)")
    plt.xlim([0, T])
    plt.ylim([0, 105])
    plt.grid(True, alpha=0.3)
    plt.show()

# Run simulation and plot
paths = run_monte_carlo(num_simulations, 100, 1.0, {})
plot_monte_carlo_results(paths)