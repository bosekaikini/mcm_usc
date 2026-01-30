import matplotlib.pyplot as plt
import numpy as np


"""
TODO
1) Define battery drain parameters based on BatteryML data
2) For baseline only, find the mean lifespan in hours
3) Sensitivity analysis then standardize for each 

Improvements:
1) Introduce noise into the battery drain and make stochastic
2) Remove the lifespan and keep more of a elastic function (further after that more stress to revert to mean)
3) Change method of computing time from the SOC
"""

# Step 0: Finding the battery drain (currently deterministic)

#Using BatteryML for Lithium Ion batteries and phone specifics
def get_battery_drain(screenPower=True, screenSize=6, cpuPower=False, voltageUse=False, batteryHistory=False):
    #Coefficients obtained from BatteryML research paper
    screenCoeff=0.5
    cpuCoeff=0.3
    voltageCoeff=0.1
    batteryHistoryCoeff=0.1
    return screenPower*screenCoeff*screenSize + cpuPower*cpuCoeff +  voltageUse*voltageCoeff + batteryHistory*batteryHistoryCoeff

batteryDrainConstant=get_battery_drain() #unit is miliamperes per hour
stateOfChargeAxis=np.linspace(0,100)
timeInHours=np.linspace(0, 25)
totalBatteryLife=10 # in hours
num_trials=1

# Step 1: State of Charge vs Time curve

# Chose the exponential decay function since the battery time to empty plots look like this on actual research
# Also, intuitively it makes sense
def get_state_of_charge(timeInHours, batteryDrainConstant):
    return 254.149408254 * np.exp(-batteryDrainConstant * timeInHours) - 154.149408254

#########################################################################

# Step 2: Time to Empty vs State of Charge curve

#Just Total battery life (arbitrary right now) - SOC^-1
def get_time_to_empty(batteryDrainConstant, stateOfChargeAxis):
    return totalBatteryLife + np.log((stateOfChargeAxis + 154.149408254) / 254.149408254) / batteryDrainConstant



#########################################################################

# Step 3: Battery Drain Parameter variation curve
#Also, run the plots


for i in range(num_trials):
    batteryDrainConstant=0.05 + i*0.02
    plt.figure()
    plt.subplot(211)
    plt.xlabel("Time (hour)")
    plt.xlim([0,20])
    plt.ylim([0,100])
    plt.ylabel("State of charge (%)")
    plt.title("Time vs State of Charge ")
    plt.plot(timeInHours, get_state_of_charge(timeInHours, batteryDrainConstant))
    
    plt.subplot(212)
    plt.xlabel("State of Charge (%)")
    plt.xlim([0,100])
    plt.ylim([0,20])
    plt.ylabel("Time to Empty (hour)")
    plt.plot(stateOfChargeAxis,get_time_to_empty(batteryDrainConstant, stateOfChargeAxis))
    plt.title("Baseline battery curve simulations")

    plt.savefig(f"batteryDrainConstant{i}.png")
    plt.show()
    
#######################################

# Step 4: Error and Sensitivity analysis

# Error metric -distance in 2d plane
def get_error(true_time_to_empty, predicted_time_to_empty):
    return abs(true_time_to_empty - predicted_time_to_empty) / true_time_to_empty * 100
