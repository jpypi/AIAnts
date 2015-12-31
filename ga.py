import random
from copy import copy as _copy

from chromosome import Chromosome

class DistBreeder(object):
    def __init__(self, crossover_rate, mutation_rate):
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

    def Breed(self, parent1, parent2):
        child1 = []
        child2 = []
        for i in xrange(len(parent1)):
            if random.random() < self.crossover_rate:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])

        return child1, child2

#    def BreedCross(self, parent1, parent2):


# Mutation rate is suggested to between 0.05 and 0.2
class RealGeneticAlg(DistBreeder):
    def __init__(self, crossover_rate = 0.5, mutation_rate = 0.1,
                    perturbation_bounds = (0.05, 0.1)):
        super(RealGeneticAlg, self).__init__(crossover_rate, mutation_rate)

        self.perturbation_bounds = perturbation_bounds

    def NewPopulation(self, old_population):
        new_population = []
        try:
            while len(new_population) < len(old_population):
                # Select two parents
                mom = RouletteSelect(old_population)
                dad = RouletteSelect(old_population)

                # Breed parents, mutate and add both children to new population
                new_population.extend(map(self.Mutate,self.Breed(mom, dad)))

            return new_population
        except:
            print old_population

    def Mutate(self, chromosome):
        for i in xrange(len(chromosome)):
            chromosome[i] += random.choice((1, -1)) *\
                             ClampRandom(*self.perturbation_bounds)
        return chromosome


def RouletteSelect(population):
    n = random.random()
    last = 0
    total = sum(map(lambda x: x.score, population))
    if total != 0:
        for chromosome in population:
            score = chromosome.score
            if last < n and n <= (last + score):
                return chromosome
            last += score
    else:
        return random.choice(population)


def ClampRandom(low, high):
    n = random.random()
    if n > high:
        n = high
    if n < low:
        n = low

    return n
