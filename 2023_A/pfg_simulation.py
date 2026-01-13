import random
import matplotlib.pyplot as plt

class PlantFunctionalGroup:
    def __init__(self, name, drought_resistance, growth_rate, reproductive_strategy):
        self.name = name
        self.drought_resistance = drought_resistance  # Scale of 1-10
        self.growth_rate = growth_rate  # Scale of 1-10
        self.reproductive_strategy = reproductive_strategy  # 'annual' or 'perennial'
        self.population = 100  # Initial population

    def __repr__(self):
        return f"{self.name}(Drought Resistance: {self.drought_resistance}, Growth Rate: {self.growth_rate}, Reproductive Strategy: {self.reproductive_strategy}, Population: {self.population})"

    def calculate_fitness(self, weather):
        """Calculate fitness modifier based on weather and traits"""
        fitness = 1.0  # Base fitness
        
        if weather == 'drought':
            # Drought resistance helps during droughts
            fitness *= 0.5 + (self.drought_resistance / 20.0)  # Range: 0.5 to 1.0
        elif weather == 'flood':
            # High growth rate helps during floods
            fitness *= 0.5 + (self.growth_rate / 20.0)  # Range: 0.5 to 1.0
        else:  # normal
            # Normal conditions favor high growth rate
            fitness *= 0.8 + (self.growth_rate / 50.0)  # Range: 0.8 to 1.0
        
        # Perennials are more stable, annuals can grow faster
        if self.reproductive_strategy == 'perennial':
            fitness *= 1.1  # Slight advantage
        
        return fitness

    def update_population(self, weather, total_population):
        """Update population based on weather and competition"""
        fitness = self.calculate_fitness(weather)
        
        # Growth/decline based on fitness and competition
        growth_factor = 0.95 + (fitness * 0.2)  # Range: 0.95 to 1.15
        self.population = int(self.population * growth_factor)
        
        # Ensure population doesn't go below 0
        self.population = max(0, self.population)


def generate_random_pfgs(num_pfgs, initial_population=100):
    """Generate random PFGs with specified initial population"""
    pfgs = []
    for i in range(num_pfgs):
        name = f"PFG_{i+1}"
        drought_resistance = random.randint(1, 10)
        growth_rate = random.randint(1, 10)
        reproductive_strategy = random.choice(['annual', 'perennial'])
        pfg = PlantFunctionalGroup(name, drought_resistance, growth_rate, reproductive_strategy)
        pfg.population = initial_population
        pfgs.append(pfg)
    return pfgs


def simulate_weather_cycles(num_cycles, irregular_probability=0.3):
    """Simulate weather cycles with potential for irregular patterns"""
    weather_data = []
    for _ in range(num_cycles):
        if random.random() < irregular_probability:
            # Irregular weather
            weather_pattern = random.choice(['flood', 'drought', 'severe_drought'])
        else:
            # Normal weather
            weather_pattern = 'normal'
        weather_data.append(weather_pattern)
    return weather_data


def run_simulation(num_pfgs, num_years, initial_population=100, irregular_probability=0.3):
    """Run the full simulation and track populations over time"""
    pfgs = generate_random_pfgs(num_pfgs, initial_population)
    weather_data = simulate_weather_cycles(num_years, irregular_probability)
    
    # Track population history
    population_history = {pfg.name: [] for pfg in pfgs}
    weather_history = []
    
    print(f"\n{'='*80}")
    print(f"SIMULATION: {num_pfgs} PFGs over {num_years} years")
    print(f"{'='*80}")
    print(f"\nInitial PFGs:")
    for pfg in pfgs:
        print(f"  {pfg}")
    
    # Run simulation for each year
    for year, weather in enumerate(weather_data):
        weather_history.append(weather)
        
        # Update each PFG's population based on weather
        for pfg in pfgs:
            pfg.update_population(weather, sum(p.population for p in pfgs))
            population_history[pfg.name].append(pfg.population)
        
        # Print yearly summary every 10 years or at the end
        if (year + 1) % max(1, num_years // 10) == 0 or year == num_years - 1:
            print(f"\nYear {year + 1} (Weather: {weather}):")
            for pfg in pfgs:
                print(f"  {pfg.name}: {pfg.population} individuals")
    
    return pfgs, population_history, weather_data


def plot_population_dynamics(population_history, pfg_names, title="PFG Population Dynamics Over Time"):
    """Plot the population dynamics of all PFGs"""
    plt.figure(figsize=(14, 8))
    
    for pfg_name in pfg_names:
        plt.plot(population_history[pfg_name], marker='o', label=pfg_name, linewidth=2)
    
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Population', fontsize=12)
    plt.title(title, fontsize=14)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == '__main__':
    # Experiment with different diversity levels
    diversity_levels = [3, 5, 10]
    
    for num_pfgs in diversity_levels:
        pfgs, population_history, weather_data = run_simulation(
            num_pfgs=num_pfgs,
            num_years=100,
            initial_population=100,
            irregular_probability=0.3
        )
        
        # Plot results
        pfg_names = [pfg.name for pfg in pfgs]
        plot_population_dynamics(population_history, pfg_names, 
                                 title=f"Population Dynamics: {num_pfgs} PFGs")
        
        # Print final summary
        print(f"\n{'='*80}")
        print(f"FINAL SUMMARY ({num_pfgs} PFGs):")
        print(f"{'='*80}")
        for pfg in pfgs:
            final_pop = population_history[pfg.name][-1]
            avg_pop = sum(population_history[pfg.name]) / len(population_history[pfg.name])
            print(f"{pfg.name}: Final Population = {final_pop}, Average = {avg_pop:.1f}")
        print()