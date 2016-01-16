import random
from copy import copy as _copy

from chromosome import Chromosome


# Gene mixing (every gene) type breeding
class SwapBreeder(object):
    def __init__(self, crossover_rate = 0.5):
        self.crossover_rate = crossover_rate

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


# "Crossover" type chromosome breeding
class CrossoverBreeder(object):
    def __init__(self, crossover_rate = 0.7):
        self.crossover_rate = crossover_rate

    def Breed(self, mom, dad):
        # Shall we do crossover?
        if random.random() > self.crossover_rate and mom == dad:
            return mom, dad

        # Pick crossover point
        i = random.randrange(0, len(mom))

        child1 = mom[:i]
        child1.extend(dad[i:])

        child2 = dad[:i]
        child2.extend(dad[i:])

        return Chromosome(child1), Chromosome(child2)


# Mutation rate is suggested to between 0.05 and 0.2 (from ai-junki.com) for
# real number alleles
class RealGeneticAlg(SwapBreeder):
    def __init__(self, crossover_rate = 0.5, mutation_rate = 0.15,
                       perturbation_bounds = (0.05, 0.1), elite = 4):
        super(RealGeneticAlg, self).__init__(crossover_rate)

        self.mutation_rate = mutation_rate

        self.perturbation_bounds = perturbation_bounds
        self.n_elite = elite

    def NewPopulation(self, old_population):
        old_population = sorted(old_population)
        new_population = []
        # Do some elitism
        new_population.extend(old_population[-self.n_elite:])
        # Mark these old best performers as such
        for c in new_population:
            c.is_top_performer = True

        # Build up a new population
        while len(new_population) < len(old_population):
            # Select two parents
            mom = RouletteSelect(old_population)
            dad = RouletteSelect(old_population)

            # Breed parents, mutate and add both children to new population
            new_population.extend(map(self.Mutate,self.Breed(mom, dad)))

        return new_population

    def Mutate(self, chromosome):
        for i in xrange(len(chromosome)):
            chromosome[i] += random.choice((1, -1)) * \
                             random.random()*self.perturbation_bounds[1]
                             #ClampRandom(*self.perturbation_bounds)
        return chromosome


# Based off code at ai-junki.com
def RouletteSelect(population):
    total = sum(map(lambda x: x.score, population))
    pie_slice = random.random() * total
    last = 0
    for chromosome in population:
        last += chromosome.score
        if last >= pie_slice:
            return chromosome


def MyRouletteSelect(population):
    n = random.random()
    last = 0
    total = float(sum(map(lambda x: x.score, population)))
    if total != 0:
        for chromosome in sorted(population, key = lambda x: x.score):
            score = chromosome.score/total
            if last < n and n <= (last + score):
                return chromosome
            last += score
    else:
        print("Huston, we have a problem!")
        return random.choice(population)


def ClampRandom(low, high):
    n = random.random()
    if n > high:
        n = high
    if n < low:
        n = low

    return n
