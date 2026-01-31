import matplotlib.pyplot as plt
import numpy as np

# Battery drain constant
def get_battery_drain(voltageUse=4.5, batteryHistory=0.5):
    voltageCoeff=0.1
    batteryHistoryCoeff=0.1
    return voltageCoeff*voltageUse + batteryHistoryCoeff*batteryHistory

batteryDrainConstant = get_battery_drain()

def drift_soc(SOC):
    return -batteryDrainConstant * (SOC + 154.149408254) # differentiate earlier

def diffusion_soc(SOC):
    noise_level = 0.25
    return noise_level * np.sqrt(np.maximum(SOC, 0.01)) #proportional according to gaussian

def drift_tte(SOC, TTE):
    theoretical_tte = np.log((SOC + 154.149408254) / 154.149408254) / batteryDrainConstant # substantial correlaiton to the theoretical
    mean_reversion = 0.5  # elasticity
    return -mean_reversion * (TTE - theoretical_tte)

def diffusion_tte(SOC):
    noise_level = 0.15 # lower than before
    return noise_level * np.sqrt(np.maximum(SOC / 100, 0.01))

totalBatteryLife = np.log(254.149408254 / 154.149408254) / batteryDrainConstant

# Time discretization for sde solver and rk4
T = totalBatteryLife * 1.2
N = 50000  # more steps for rungekutta
dt = T / N
timeInHours = np.linspace(0, T, N)

# runge kutts
def rk4_step_soc(SOC, t, dt):
    k1_drift = drift_soc(SOC)
    k1_diff = diffusion_soc(SOC)
    dW = np.random.normal(0, np.sqrt(dt))
    
    k2_drift = drift_soc(SOC + 0.5*k1_drift*dt)
    k2_diff = diffusion_soc(SOC + 0.5*k1_diff*dW*0.5)
    
    k3_drift = drift_soc(SOC + 0.5*k2_drift*dt)
    k3_diff = diffusion_soc(SOC + 0.5*k2_diff*dW*0.5)
    
    k4_drift = drift_soc(SOC + k3_drift*dt)
    k4_diff = diffusion_soc(SOC + k3_diff*dW)
    drift_avg = (k1_drift + 2*k2_drift + 2*k3_drift + k4_drift) / 6
    diff_avg = (k1_diff + 2*k2_diff + 2*k3_diff + k4_diff) / 6
    #BOIIIIIIIIIIIIIIIIIIIIIIII
    SOC_new = SOC + drift_avg * dt + diff_avg * dW
    return np.clip(SOC_new, 0, 100), dW

def rk4_step_tte(SOC, TTE, t, dt, dW):
    #on some same shit as before
    k1_drift = drift_tte(SOC, TTE)
    k1_diff = diffusion_tte(SOC)
    
    k2_drift = drift_tte(SOC, TTE + 0.5*k1_drift*dt)
    k2_diff = diffusion_tte(SOC)
    
    k3_drift = drift_tte(SOC, TTE + 0.5*k2_drift*dt)
    k3_diff = diffusion_tte(SOC)
    
    k4_drift = drift_tte(SOC, TTE + k3_drift*dt)
    k4_diff = diffusion_tte(SOC)
    
    drift_avg = (k1_drift + 2*k2_drift + 2*k3_drift + k4_drift) / 6
    diff_avg = (k1_diff + 2*k2_diff + 2*k3_diff + k4_diff) / 6
    
    TTE_new = TTE + drift_avg * dt + diff_avg * dW
    return np.clip(TTE_new, 0, totalBatteryLife * 1.2)

# plot some shit
SOC = np.zeros(N)
SOC[0] = 100

for i in range(1, N):
    SOC[i], _ = rk4_step_soc(SOC[i-1], timeInHours[i-1], dt)

# Deterministic SOC for comparison
SOC_deterministic = 254.149408254 * np.exp(-batteryDrainConstant * timeInHours) - 154.149408254

# SOC & TTE
stateOfChargeAxis = np.linspace(0, 100, 1000)

# Use coupled RK4 for accurate TTE trajectory
SOC_path = np.linspace(100, 0.5, 5000)
TTE_path = np.zeros(5000)
TTE_path[0] = totalBatteryLife

dt_soc = 100 / 5000  # SOC step 
for i in range(1, 5000):
    SOC_curr = SOC_path[i-1]
    TTE_curr = TTE_path[i-1]
    dW_local = np.random.normal(0, 1) 
    
    TTE_path[i] = rk4_step_tte(SOC_curr, TTE_curr, 0, dt_soc, dW_local * np.sqrt(dt_soc))

time_to_empty_stochastic = np.interp(stateOfChargeAxis, SOC_path[::-1], TTE_path[::-1])
time_to_empty_deterministic = np.log((stateOfChargeAxis + 154.149408254) / 154.149408254) / batteryDrainConstant

# for reproducibility
np.random.seed(42)
fig = plt.figure(figsize=(12, 9))

# Plot 1: SOC vs Time
plt.subplot(211)
plt.title("SOC vs TTE")
plt.xlabel("Time (hours)")
plt.ylabel("State of Charge (%)")
plt.xlim([0, totalBatteryLife * 1.1])
plt.ylim([0, 105])
plt.grid(True, alpha=0.3)
plt.plot(timeInHours, SOC_deterministic)
plt.plot(timeInHours, SOC)

# Plot 2nd
plt.subplot(212)
plt.title("TTE vs SOC")
plt.xlabel("State of Charge (%)")
plt.ylabel("Time to Empty (hours)")
plt.xlim([0, 100])
plt.ylim([0, totalBatteryLife * 1.15])
plt.grid(True, alpha=0.3)
plt.plot(stateOfChargeAxis, time_to_empty_deterministic)
plt.plot(stateOfChargeAxis, time_to_empty_stochastic)
plt.legend(fontsize=10)

plt.tight_layout()
plt.savefig("battery_stochastic_curve.png", dpi=300)
plt.show()