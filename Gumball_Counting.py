## Gumball Counting Project ##
import math
import numpy as np
from scipy.stats import norm, sem, t
import matplotlib.pyplot as plt

# Total gumballs: 659


def volume_of_cylinder(height, circumference):
    # V =  πr^2h
    ## NOTE: r = C/(2*pi)
    radius = circumference/(2*math.pi)
    return math.pi * (radius ** 2) * height


def volume_of_sphere(diameter):
    # V = 4/3πr^3 
    ## NOTE: r = C/(2*pi)
    radius = diameter/2
    return (4/3) * math.pi * radius**3


def estimate_gumballs_in_jar(jar_height, jar_diameter, gumball_diameter, jar_fill_percentage, packing_efficiency):
    jar_volume = volume_of_cylinder(jar_height, jar_diameter)
    gumball_volume = volume_of_sphere(gumball_diameter) # Assuming gumballs are perfectly cylindrical
    
    # The volume of space in the jar that the gumballs can fill is 
    # the jar's volume times the packing efficiency times the fill percentage
    space_for_gumballs = jar_volume * packing_efficiency * jar_fill_percentage
    
    # Now we can find how many gumballs can fit in this space
    estimated_gumballs = space_for_gumballs / gumball_volume
    return estimated_gumballs


def simulate_gumball_estimations(jar_height, jar_diameter, gumball_diameter, jar_fill_percentage, num_simulations):
    # Store the results of all simulations here
    all_estimations = []

    for _ in range(num_simulations):
        # Sample packing efficiency from a beta distribution 
        # Shift and scale to be in the range [0.64, 0.74]
        packing_efficiency = 0.64 + np.random.beta(a=2, b=5) * 0.1

        # Randomly vary gumball diameter by +/- 10%
        varied_gumball_diameter = gumball_diameter * np.random.uniform(0.99, 1.01)

        estimation = estimate_gumballs_in_jar(jar_height, 
                                              jar_diameter, 
                                              varied_gumball_diameter, 
                                              jar_fill_percentage, 
                                              packing_efficiency)
        all_estimations.append(estimation)
    
    # Calculate standard error of the mean (SEM) and 95% Confidence Interval
    mu = np.mean(all_estimations)
    std = np.std(all_estimations)
    med = np.median(all_estimations)
    standard_error = sem(all_estimations)
    confidence_interval = t.interval(confidence=0.95, 
                                     df=len(all_estimations)-1, 
                                     loc=mu, 
                                     scale=standard_error)
    return all_estimations, mu, std, med, standard_error, confidence_interval, packing_efficiency


def plot_histogram_with_distribution(all_estimations, mu, std, num_simulations):
    # Fit a normal distribution to the data
    _, _ = norm.fit(all_estimations)
    
    # Plot the histogram
    plt.hist(all_estimations, bins=25, density=True, alpha=0.6, color='g')

    # Plot the distribution
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)

    # Add a red dashed line at the mean (apex of the distribution)
    plt.axvline(mu, color='r', linestyle='dashed', linewidth=2)
    
    plt.title(f"Fit Results for {num_simulations} Runs")
    plt.show()


def box_and_whisker_plot(all_estimations):
    plt.figure(figsize=(10,6))
    plt.boxplot(all_estimations, vert=False)
    plt.title('Box and Whisker Plot of Estimations')
    plt.xlabel('Estimated Number of Gumballs')
    plt.show()


def plot_cdf(all_estimations):
    plt.figure(figsize=(10,6))
    values, base = np.histogram(all_estimations, bins=40)
    cumulative = np.cumsum(values) / np.sum(values)
    plt.plot(base[:-1], cumulative)

    # Adding the red dashed lines for median
    median = np.median(all_estimations)
    plt.axvline(median, color='r', linestyle='dashed', linewidth=2)
    plt.axhline(0.5, color='r', linestyle='dashed', linewidth=2)

    plt.title('Cumulative Distribution Function (CDF) of Estimations')
    plt.xlabel('Estimated Number of Gumballs')
    plt.ylabel('Cumulative Probability')
    plt.show()
    

def run_and_plot(jar_height, jar_diameter, gumball_diameter, jar_fill_percentage, simulation_counts):
    results = []
    for i, num_simulations in enumerate(simulation_counts, start=1):
        all_estimations, mu, std, med, sem, ci, packing_efficiency = simulate_gumball_estimations(jar_height, 
                                                                                                  jar_diameter, 
                                                                                                  gumball_diameter, 
                                                                                                  jar_fill_percentage, 
                                                                                                  num_simulations)
        
        # Uncomment the following lines as needed to produce the different plots
        plot_histogram_with_distribution(all_estimations, mu, std, num_simulations)
        box_and_whisker_plot(all_estimations)
        #plot_cdf(all_estimations)
        
        results.append((mu, std, sem, ci))
        print(f"Run {i}: Mean = {mu:.2f}; Median = {med:.2f}, Std Dev = {std:.2f}; SEM = {sem:.2f}; CI = ({round(ci[0], 2)}, {round(ci[1], 2)})")
    return results


# Model Inputs
'''
The variable 'a' represents manual measurements of randomly selected gumballs
so an average diameter could be established. 

SEM = Standard Error of the Mean
'''
a = [15,15,15,15,16,16,16,15.5,15,15.5,15.5,15,15.5,15,15.5,15,15,15,
 15,15,15.5,15.5,15,15.5,15.5,15.5,15.5,15,15.5,15.5,15,15,15,15.5,
 15.5,15,15,15,15.5,15,15.5,15.5,15,15.5,15.5,15,15,15.5,15,15.5,
 15.5,15.5,15,15.5,15.5,15.5,16,16,15,15,15,15] # mm

avg_gumball_diameter = np.mean(a) # mm
num_simulations = [10, 100, 1000, 10000]
jar_height = 0.144 # m
free_space = 0.076 # m
used_height = jar_height - free_space # m
jar_circimference = 0.453 # m
gumball_diameter = avg_gumball_diameter/1000 # m

total_cylinder_volume = volume_of_cylinder(jar_height,jar_circimference) # m^3
used_cylinder_volume = volume_of_cylinder(used_height,jar_circimference) # m^3
jar_fill_percentage = (used_cylinder_volume/total_cylinder_volume) * 0.7

means = run_and_plot(jar_height, jar_circimference, gumball_diameter, 
                     jar_fill_percentage, 
                     num_simulations)

actual_gumball_count = 97+83+104
predicted_gumball_count = int(np.floor(means[3][0]))
experimental_accuracy = (predicted_gumball_count/actual_gumball_count)*100
print(f"Experimental Accuracy: {experimental_accuracy:.2f}%")
