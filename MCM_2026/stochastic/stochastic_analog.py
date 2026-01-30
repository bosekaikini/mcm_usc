import matplotlib.pyplot as plt
import numpy as np
import tqdm

"""
TODO
1) Introduce noise into the battery drain and make stochastic
2) Remove the lifespan and keep more of a elastic function (further after that more stress to revert to mean)
3) Change method of computing time from the SOC
"""

# Step 0: Finding the battery drain (currently deterministic)

#Using BatteryML for Lithium Ion batteries and phone specifics
def get_battery_drain(screenPower=True, screenSize=6, cpuPower=False, networkPower=False, batteryHistory=False):
    #Coefficients obtained from BatteryML research paper
    screenCoeff=0.5
    cpuCoeff=0.3
    networkCoeff=0.1
    batteryHistoryCoeff=0.1
    w_t=0.5 # noise
    age=0.1 #capacity degradation and battery decay factor
    return screenPower*screenCoeff*screenSize + cpuPower*cpuCoeff + networkPower*networkCoeff + batteryHistory*batteryHistoryCoeff

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



