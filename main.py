#!/usr/bin/env python2

# Many thanks to this guy:
# http://www.akeric.com/blog/?p=1527

import sys
import random
import copy

import pyglet
from pyglet.window import key

from vector import Vector
from ant import Ant, PRO_ANT_IMAGE
from food import Food, Poison

import ga
from chromosome import Chromosome


class SpriteWindow(pyglet.window.Window):
    def __init__(self, size, caption="Pyglet game", fps=60):
        super(SpriteWindow, self).__init__(width=size[0], height=size[1],
                                           caption=caption)
        self.width = size[0]
        self.height = size[1]

        # Set the background color
        self.setBackgroundColor()

        self.sprite_batch = pyglet.graphics.Batch()
        self.ants = []
        self.food = []
        self.poision = [
                        Poison(self, (size[0]/4,     size[1]/4), self.sprite_batch),
                        Poison(self, (size[0]/4,   3*size[1]/4), self.sprite_batch),
                        Poison(self, (3*size[0]/4,   size[1]/4), self.sprite_batch),
                        Poison(self, (3*size[0]/4, 3*size[1]/4), self.sprite_batch)
                       ]

        self.num_food = 25
        self.num_ants = 30

        self.growFood()

        self.step = 0
        self.generations = 0
        self.population_change_steps = 1000

        pyglet.clock.schedule_interval(self.update, 1.0/fps)

        self.ga = ga.RealGeneticAlg(
                                    perturbation_bounds = (0.01, 0.3),
                                    crossover_rate = 0.7,
                                    mutation_rate = 0.2,
                                    elite = 6
                                   )


    @staticmethod
    def setBackgroundColor(color=(0.9, 0.9, 0.9, 1)):
        if len(color) != 4:
            raise ValueError, "Color must be of length 4!"
        pyglet.gl.glClearColor(*color)


    @staticmethod
    def run():
        pyglet.app.run()

    def on_draw(self):
        self.clear()
        self.sprite_batch.draw()


    def on_text(self, symbol):
        if symbol == "s":
            print "Saving weights"
            with open("net_weights.txt", "w") as f:
                for a in self.ants:
                    f.write(",".join(map(str, a.neural_net.GetWeights())) + "\n")

        if symbol == "l":
            print "Loading weights"
            with open("net_weights.txt") as f:
                for ant in self.ants:
                    ant.neural_net.SetWeights(map(float,f.readline().split(",")))

        if symbol == "f":
            self.fastMode(2)


    def fastMode(self, generations = 1):
        stop_generation = self.generations + generations
        while self.generations < stop_generation:
            self.update(1)


    # dt is "delta time" since last update
    def update(self, dt):
        self.step += 1

        for ant in self.ants:
            ant.update(0.5, self.food, self.poision)
            for food in self.food:
                if not food.eaten and ant.collidesWith(food):
                    food.eaten = True
                    ant.score += 1

            for poison in self.poision:
                if ant.collidesWith(poison):
                    ant.score -= 3

        self.food = filter(lambda f: not f.eaten, self.food)

        self.growFood()

        if self.step > self.population_change_steps:
            self.generations += 1
            self.printStats()

            self.step = 0
            self.updateNets(self.ga.NewPopulation(self.chromosomesFromAnts()))


    def printStats(self):
        avg_score = 0
        max_score = 0
        min_score = None
        for a in self.ants:
            avg_score += a.score
            if a.score > max_score:
                max_score = a.score
            if min_score == None or a.score < min_score:
                min_score = a.score

        print self.generations, min_score, max_score, avg_score/float(self.num_ants)


    def chromosomesFromAnts(self):
        return [Chromosome(a.neural_net.GetWeights(), a.score) for a in self.ants]

    def updateNets(self, chromosomes):
        for i in xrange(self.num_ants):
            self.ants[i].score = 0
            #self.ants[i].updateImage(chromosomes[i].is_top_performer)
            self.ants[i].neural_net.SetWeights(chromosomes[i])

    def getRandomPoint(self, margin = 0):
        return (random.randrange(margin ,self.width - margin),
                random.randrange(margin, self.height - margin))

    def growFood(self):
        while len(self.food) < self.num_food:
            #point = (random.randrange(0,100), random.randrange(0,100))
            point = self.getRandomPoint(10)
            self.food.append(Food(self, point, self.sprite_batch))

    def initAnts(self):
        for i in xrange(self.num_ants):
            a = random.randrange(0, 359)
            self.ants.append(Ant(self, self.getRandomPoint(),
                                 Vector(20, a), self.sprite_batch))




if __name__ == "__main__":
    import cProfile
    window = SpriteWindow((400,400), fps = 240)
    window.initAnts()
    #cProfile.run("window.update(1, 20)")
    #window.fastMode(10)
    sys.exit(window.run())
