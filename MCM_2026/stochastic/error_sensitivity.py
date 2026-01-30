# Step 4: Error and Sensitivity analysis

#Use real sensitivity analysis
# monte carlo (SD error, not MSE now that were in stochastic)
# Also using stability analysis for the plot

# Error metric -distance in 2d plane
def get_error(true_time_to_empty, predicted_time_to_empty):
    return abs(true_time_to_empty - predicted_time_to_empty) / true_time_to_empty * 100