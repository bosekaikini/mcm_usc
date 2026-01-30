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