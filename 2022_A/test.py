import power_calculator
import track

track=track.generate_track(n_points=1000, total_length=5000.0)
results = power_calculator.calculate_next_optimal_power_value(395.3, 31.8, 22.0, 600, track)
p_func = power_calculator.get_optimal_power_function(results, track)
power_calculator.plot_optimal_power_function(p_func, 10000.0)

#total velocity=768.5 seconds




