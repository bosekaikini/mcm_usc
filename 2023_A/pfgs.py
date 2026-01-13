import numpy as np



def generate_random_pfgs(num_pfgs, num_traits, attributes):
    pfgs = [[]]
    for pfg in range(num_pfgs):
        for trait in range(num_traits):
            trait=np.random.choice(attributes[trait])
            pfgs[pfg].append(trait)
    return pfgs
    

def weather_cycle(skew, regular_drought_factor):
    if skew!=0:
        return np.random()