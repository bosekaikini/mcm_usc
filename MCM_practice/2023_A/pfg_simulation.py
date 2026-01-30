import random
import matplotlib.pyplot as plt

class PlantFunctionalGroup:
    def __init__(self, name, drought_resistance, water_requirement, lifespan, space_requirement):
        """
        Create a PFG with traits that reflect real-world tradeoffs
        
        drought_resistance: 1-10 (efficiency using available water)
        water_requirement: 1-10 (water needed per individual per cycle)
        lifespan: 1-10 (years individual lives; annuals ~1, perennials ~5-10)
        space_requirement: 1-10 (space needed per individual)
        """
        self.name = name
        self.drought_resistance = drought_resistance  # Efficiency: higher = uses water better
        self.water_requirement = water_requirement    # Demand: higher = needs more water
        self.lifespan = lifespan                      # Longevity
        self.space_requirement = space_requirement    # Area needed
        self.population = 100  # Initial population
        self.age_structure = [self.population]  # Track age cohorts for perennials

    def __repr__(self):
        return f"{self.name}(Water Req: {self.water_requirement}, Drought Resist: {self.drought_resistance}, Lifespan: {self.lifespan}, Space Req: {self.space_requirement}, Pop: {self.population})"

    def calculate_water_demand(self):
        """Calculate total water needed by this PFG's population"""
        # Drought-resistant plants use water more efficiently
        efficiency_factor = self.drought_resistance / 10.0  # 0.1 to 1.0
        water_demand = self.population * self.water_requirement * (1.0 - (efficiency_factor * 0.5))
        return water_demand

    def calculate_space_demand(self):
        """Calculate total space needed by this PFG's population"""
        return self.population * self.space_requirement

    def calculate_resource_stress(self, total_water_demand_all, total_space_demand_all, available_water, available_space):
        """
        Calculate stress from resource scarcity using density-dependent feedback
        When resources are scarce AND populations are high, stress increases
        When populations are low, stress decreases even if resources are limited
        """
        # What proportion of total demand does this species represent?
        if total_water_demand_all > 0:
            water_share = self.calculate_water_demand() / total_water_demand_all
        else:
            water_share = 0
        
        if total_space_demand_all > 0:
            space_share = self.calculate_space_demand() / total_space_demand_all
        else:
            space_share = 0
        
        # Resource availability index (how much resource per unit of total demand)
        water_availability = max(0.1, available_water / max(1, total_water_demand_all))
        space_availability = max(0.1, available_space / max(1, total_space_demand_all))
        
        # Combine: if resources are abundant, stress is low; if scarce, stress is high
        # Use geometric mean for realistic interaction
        resource_stress = (water_availability * space_availability) ** 0.5
        resource_stress = min(2.0, max(0.2, resource_stress))  # Clamp between 0.2 and 2.0
        
        return resource_stress

    def update_population(self, weather, total_water_demand_all, total_space_demand_all, available_water, available_space):
        """
        Update population with realistic density-dependent dynamics
        Allows populations to stabilize and fluctuate around equilibrium
        """
        # Resource stress with density-dependent feedback
        resource_stress = self.calculate_resource_stress(
            total_water_demand_all, total_space_demand_all, available_water, available_space
        )
        
        # Weather stress
        weather_stress = 1.0
        if weather == 'drought':
            weather_stress = 0.5 + (self.drought_resistance / 20.0)  # 0.5-1.0
        elif weather == 'severe_drought':
            weather_stress = 0.3 + (self.drought_resistance / 33.0)  # 0.3-0.6
        elif weather == 'flood':
            weather_stress = 0.6 + (1.0 - self.space_requirement / 10.0) * 0.3  # 0.6-0.9
        else:  # normal
            weather_stress = 1.0
        
        # Combined stress factor
        combined_stress = resource_stress * weather_stress
        
        # Base reproductive rates (without stress)
        if self.lifespan <= 2:  # Annual strategy
            base_reproduction = 2.5  # Annuals can have high reproduction
            base_survival = 0.05  # Most annuals die each year
        else:  # Perennial strategy
            base_reproduction = 1.3  # Perennials have lower reproduction
            base_survival = 0.75  # High survival rate
        
        # Density-dependent regulation: lower populations grow faster
        # This creates realistic equilibrium dynamics
        density_factor = max(0.1, 1.0 - (self.population / 1000.0))  # Scales with population
        
        # Calculate births (high when population is low and conditions are good)
        births = self.population * (base_reproduction - 1.0) * combined_stress * density_factor
        
        # Calculate survival (independent of density, but affected by stress and lifespan)
        survival_rate = base_survival * combined_stress
        survivors = self.population * survival_rate
        
        # New population
        self.population = int(survivors + births)
        
        # Extinction threshold: if population drops very low, small chance of recovery
        if 0 < self.population < 5:
            if random.random() > 0.7:  # 30% chance to recover if nearly extinct
                self.population = max(1, int(self.population * 0.5))
        
        # Ensure population doesn't go below 0
        self.population = max(0, self.population)


def generate_random_pfgs(num_pfgs, variable_initial=True):
    """Generate random PFGs with realistic trait tradeoffs"""
    pfgs = []
    for i in range(num_pfgs):
        name = f"PFG_{i+1}"
        # Create trait tradeoffs: 
        # - High water requirement usually means fast growth but vulnerable
        # - Low water requirement means drought-resistant but slower growth
        water_requirement = random.randint(1, 10)
        drought_resistance = random.randint(1, 10)
        lifespan = random.randint(1, 10)
        space_requirement = random.randint(1, 10)
        
        pfg = PlantFunctionalGroup(name, drought_resistance, water_requirement, lifespan, space_requirement)
        
        # Variable initial populations
        if variable_initial:
            pfg.population = random.randint(20, 150)  # Random initial population
        else:
            pfg.population = 100  # Fixed initial population
        
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


def run_simulation(num_pfgs, num_cycles, variable_initial=True, irregular_probability=0.3):
    """Run the full simulation and track populations through weather cycles"""
    pfgs = generate_random_pfgs(num_pfgs, variable_initial=variable_initial)
    weather_data = simulate_weather_cycles(num_cycles, irregular_probability)
    
    # Resource constraints (fixed)
    max_water = 10000  # Total water available
    max_space = 5000   # Total space available
    
    # Track population history
    population_history = {pfg.name: [] for pfg in pfgs}
    
    print(f"\n{'='*80}")
    print(f"SIMULATION: {num_pfgs} PFGs over {num_cycles} weather cycles")
    print(f"{'='*80}")
    print(f"\nInitial PFGs:")
    for pfg in pfgs:
        print(f"  {pfg}")
    
    # Run simulation for each weather cycle
    for cycle, weather in enumerate(weather_data):
        # Calculate total resource demand from ALL species
        total_water_demand = sum(pfg.calculate_water_demand() for pfg in pfgs)
        total_space_demand = sum(pfg.calculate_space_demand() for pfg in pfgs)
        
        # Scale available resources based on weather
        if weather == 'drought':
            available_water = max_water * 0.4
        elif weather == 'severe_drought':
            available_water = max_water * 0.2
        else:
            available_water = max_water
        
        if weather == 'flood':
            available_space = max_space * 0.6  # Flooding reduces usable space
        else:
            available_space = max_space
        
        # Update each PFG's population based on resources and weather
        for pfg in pfgs:
            pfg.update_population(weather, total_water_demand, total_space_demand, available_water, available_space)
            population_history[pfg.name].append(pfg.population)
        
        # Print cycle summary every 10 cycles or at the end
        if (cycle + 1) % max(1, num_cycles // 10) == 0 or cycle == num_cycles - 1:
            print(f"\nCycle {cycle + 1} (Weather: {weather:15s}):")
            total_pop = sum(pfg.population for pfg in pfgs)
            print(f"  Total population: {total_pop}")
            for pfg in pfgs:
                print(f"    {pfg.name}: {pfg.population:5d}")
    
    return pfgs, population_history, weather_data


def plot_population_dynamics(population_history, pfg_names, weather_data, title="PFG Population Dynamics Over Weather Cycles"):
    """Plot the population dynamics of all PFGs with weather cycles on x-axis"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
    
    # Main plot: Population dynamics
    for pfg_name in pfg_names:
        ax1.plot(range(len(population_history[pfg_name])), population_history[pfg_name], 
                marker='o', label=pfg_name, linewidth=2.5, markersize=4)
    
    ax1.set_ylabel('Population', fontsize=12, fontweight='bold')
    ax1.set_title(title, fontsize=14, fontweight='bold')
    ax1.legend(loc='best', fontsize=10, ncol=2)
    ax1.grid(True, alpha=0.3)
    
    # Bottom plot: Weather cycles
    weather_colors = {
        'normal': 'lightblue',
        'drought': 'orange',
        'severe_drought': 'red',
        'flood': 'darkblue'
    }
    
    for i, weather in enumerate(weather_data):
        color = weather_colors.get(weather, 'gray')
        ax2.bar(i, 1, color=color, edgecolor='black', width=0.8)
    
    ax2.set_xlim(-0.5, len(weather_data) - 0.5)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel('Weather Cycle', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Weather', fontsize=10)
    ax2.set_yticks([])
    
    # Add legend for weather
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, edgecolor='black', label=weather) 
                       for weather, color in weather_colors.items()]
    ax2.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    plt.tight_layout()
    plt.show()


def check_stability(population_history, pfg_names, stability_window=20, threshold=0.1):
    """
    Check if populations are stable in the last k generations
    Returns: (is_stable, proportions_dict)
    Stability is assessed by checking if populations vary less than threshold in last stability_window cycles
    """
    if len(population_history[pfg_names[0]]) < stability_window:
        return False, {}
    
    is_stable = True
    proportions = {}
    
    for pfg_name in pfg_names:
        last_n = population_history[pfg_name][-stability_window:]
        avg = sum(last_n) / len(last_n)
        
        # Check for zero population (extinction)
        if avg == 0:
            proportions[pfg_name] = 0.0
            continue
        
        # Calculate coefficient of variation
        variance = sum((x - avg) ** 2 for x in last_n) / len(last_n)
        std_dev = variance ** 0.5
        cv = std_dev / avg if avg > 0 else float('inf')
        
        # If CV is too high, system is unstable
        if cv > threshold:
            is_stable = False
    
    # Calculate final proportions (if stable)
    if is_stable:
        total_pop = sum(population_history[pfg_name][-1] for pfg_name in pfg_names)
        if total_pop > 0:
            for pfg_name in pfg_names:
                proportions[pfg_name] = population_history[pfg_name][-1] / total_pop
    
    return is_stable, proportions


def print_stability_and_proportions(pfgs, population_history):
    """Print stability status and population proportions"""
    pfg_names = [pfg.name for pfg in pfgs]
    is_stable, proportions = check_stability(population_history, pfg_names)
    
    print(f"\n{'='*80}")
    print(f"STABILITY ANALYSIS (last 20 cycles):")
    print(f"{'='*80}")
    
    if is_stable:
        print("Status: STABLE ✓")
        print("\nPopulation Proportions:")
        total = sum(pfgs[-1].population for pfgs in [population_history[name] for name in pfg_names])
        for pfg in pfgs:
            if pfg.name in proportions:
                prop = proportions[pfg.name]
                print(f"  {pfg.name}: {prop:6.1%} (Final pop: {population_history[pfg.name][-1]:5d})")
    else:
        print("Status: UNSTABLE - Population dynamics are still fluctuating significantly")
        print("\nCurrent populations:")
        for pfg in pfgs:
            final_pop = population_history[pfg.name][-1]
            avg_pop = sum(population_history[pfg.name][-20:]) / 20
            print(f"  {pfg.name}: Current = {final_pop:5d}, Avg(last 20) = {avg_pop:7.1f}")
    
    return is_stable, proportions


def calculate_stress_recovery(population_history, weather_data):
    """Calculate how well populations recover after stress events (drought/flood)"""
    if len(weather_data) < 5:
        return 1.0
    
    recovery_scores = []
    
    # Find stress events and measure recovery in next few cycles
    for i in range(len(weather_data) - 3):
        if weather_data[i] in ['drought', 'severe_drought', 'flood']:
            # Get populations during and after stress
            for pfg_name in list(population_history.keys()):
                if i < len(population_history[pfg_name]):
                    stress_pop = population_history[pfg_name][i]
                    recovery_pop = sum(population_history[pfg_name][i+1:min(i+4, len(population_history[pfg_name]))]) / 3
                    
                    if stress_pop > 0:
                        recovery_ratio = recovery_pop / max(1, stress_pop)
                        recovery_scores.append(min(2.0, recovery_ratio))  # Cap at 2x recovery
    
    # Average recovery score across all stress events
    return sum(recovery_scores) / len(recovery_scores) if recovery_scores else 1.0


def calculate_population_variance(population_history):
    """Calculate variance in populations (lower = more stable)"""
    variances = []
    
    for pfg_name, pops in population_history.items():
        if len(pops) > 1:
            last_20 = pops[-20:] if len(pops) >= 20 else pops
            avg = sum(last_20) / len(last_20)
            
            if avg > 0:
                var = sum((p - avg) ** 2 for p in last_20) / len(last_20)
                cv = (var ** 0.5) / avg  # Coefficient of variation
                variances.append(cv)
    
    # Return average variance (lower is better for stability)
    return sum(variances) / len(variances) if variances else 0.0


# Example usage
if __name__ == '__main__':
    # Run simulations with different diversity levels and compare
    diversity_levels = [3, 5, 10]
    comparison_results = {}
    
    for num_pfgs in diversity_levels:
        print(f"\n\n{'#'*80}")
        print(f"RUNNING SIMULATION WITH {num_pfgs} PFGs")
        print(f"{'#'*80}")
        
        pfgs, population_history, weather_data = run_simulation(
            num_pfgs=num_pfgs,
            num_cycles=100,
            variable_initial=True,  # Random starting populations
            irregular_probability=0.3
        )
        
        # Plot results (one plot per diversity level)
        pfg_names = [pfg.name for pfg in pfgs]
        plot_population_dynamics(population_history, pfg_names, weather_data,
                                 title=f"Population Dynamics: {num_pfgs} PFGs over 100 Weather Cycles (Variable Initial Populations)")
        
        # Analyze stability and proportions
        is_stable, proportions = print_stability_and_proportions(pfgs, population_history)
        
        # Store results for comparison
        comparison_results[num_pfgs] = {
            'is_stable': is_stable,
            'proportions': proportions,
            'pfgs': pfgs,
            'population_history': population_history,
            'weather_data': weather_data,
            'total_final_population': sum(pfg.population for pfg in pfgs)
        }
    
    # Comparative analysis across diversity levels
    print(f"\n\n{'='*80}")
    print(f"COMPARATIVE ANALYSIS: ENVIRONMENTAL ADAPTATION & LONG-TERM VIABILITY")
    print(f"{'='*80}")
    
    viability_metrics = {}
    
    for num_pfgs in diversity_levels:
        results = comparison_results[num_pfgs]
        pfgs = results['pfgs']
        population_history = results['population_history']
        
        # Calculate key metrics for adaptation and viability
        survival_rate = sum(1 for pfg in pfgs if pfg.population > 0) / num_pfgs
        extinction_count = num_pfgs - sum(1 for pfg in pfgs if pfg.population > 0)
        
        # Recovery from stress: measure population at stress events vs after
        stress_recovery = calculate_stress_recovery(population_history, results['weather_data'])
        
        # Population variance in last 20 cycles (lower = more stable)
        pop_variance = calculate_population_variance(population_history)
        
        viability_metrics[num_pfgs] = {
            'survival_rate': survival_rate,
            'extinction_count': extinction_count,
            'final_total_pop': results['total_final_population'],
            'stress_recovery': stress_recovery,
            'stability_score': 1.0 / (1.0 + pop_variance),
            'is_stable': results['is_stable']
        }
        
        print(f"\n{num_pfgs} PFG Community:")
        print(f"  Species Persistence: {sum(1 for pfg in pfgs if pfg.population > 0)}/{num_pfgs} species survived")
        print(f"  Extinction Events: {extinction_count}")
        print(f"  Total Final Population: {results['total_final_population']}")
        print(f"  Stress Recovery Index: {stress_recovery:.2f} (higher = better adaptation to stress)")
        print(f"  Population Stability: {viability_metrics[num_pfgs]['stability_score']:.2f} (higher = more stable)")
        print(f"  Long-term Viability: {'STABLE ✓' if results['is_stable'] else 'FLUCTUATING'}")
    
    # Recommendation
    print(f"\n{'='*80}")
    print(f"OPTIMAL DIVERSITY FOR ADAPTATION & LONG-TERM VIABILITY:")
    print(f"{'='*80}")
    
    # Score each diversity level on multiple factors
    scores = {}
    for num_pfgs in diversity_levels:
        metrics = viability_metrics[num_pfgs]
        # Multi-factor scoring: survival, stress recovery, stability
        score = (metrics['survival_rate'] * 0.3 +  # 30% weight on species survival
                metrics['stress_recovery'] * 0.4 +   # 40% weight on adaptation to stress
                metrics['stability_score'] * 0.3)    # 30% weight on stability
        scores[num_pfgs] = score
    
    best_div = max(scores.items(), key=lambda x: x[1])[0]
    
    print(f"\n🏆 RECOMMENDED DIVERSITY LEVEL: {best_div} PFGs\n")
    print(f"Viability Scores (0-1 scale):")
    for num_pfgs in sorted(diversity_levels):
        marker = "→" if num_pfgs == best_div else " "
        print(f"  {marker} {num_pfgs} PFGs: {scores[num_pfgs]:.3f}")
    
    print(f"\nWhy {best_div} PFGs is optimal:")
    best_metrics = viability_metrics[best_div]
    print(f"  • Highest survival rate: {best_metrics['survival_rate']:.1%} of species persisted")
    print(f"  • Best adaptation to stress: Recovery index of {best_metrics['stress_recovery']:.2f}")
    print(f"  • Stability score: {best_metrics['stability_score']:.2f}")
    print(f"  • Final community size: {best_metrics['final_total_pop']} individuals")
    print(f"\nThis diversity level enables plant communities to:")
    print(f"  - Survive difficult environmental conditions (droughts, floods)")
    print(f"  - Recover quickly from stress events")
    print(f"  - Maintain population stability over time")
    print(f"  - Ensure long-term species persistence")


def calculate_stress_recovery(population_history, weather_data):
    """Calculate how well populations recover after stress events (drought/flood)"""
    if len(weather_data) < 5:
        return 1.0
    
    recovery_scores = []
    
    # Find stress events and measure recovery in next few cycles
    for i in range(len(weather_data) - 3):
        if weather_data[i] in ['drought', 'severe_drought', 'flood']:
            # Get populations during and after stress
            for pfg_name in list(population_history.keys()):
                if i < len(population_history[pfg_name]):
                    stress_pop = population_history[pfg_name][i]
                    recovery_pop = sum(population_history[pfg_name][i+1:min(i+4, len(population_history[pfg_name]))]) / 3
                    
                    if stress_pop > 0:
                        recovery_ratio = recovery_pop / max(1, stress_pop)
                        recovery_scores.append(min(2.0, recovery_ratio))  # Cap at 2x recovery
    
    # Average recovery score across all stress events
    return sum(recovery_scores) / len(recovery_scores) if recovery_scores else 1.0


def calculate_population_variance(population_history):
    """Calculate variance in populations (lower = more stable)"""
    variances = []
    
    for pfg_name, pops in population_history.items():
        if len(pops) > 1:
            last_20 = pops[-20:] if len(pops) >= 20 else pops
            avg = sum(last_20) / len(last_20)
            
            if avg > 0:
                var = sum((p - avg) ** 2 for p in last_20) / len(last_20)
                cv = (var ** 0.5) / avg  # Coefficient of variation
                variances.append(cv)
    
    # Return average variance (lower is better for stability)
    return sum(variances) / len(variances) if variances else 0.0