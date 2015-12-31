#!/usr/local/bin/python

# Many thanks to this guy:
# http://www.akeric.com/blog/?p=1527

import sys
import random
import copy

import pyglet
from pyglet.window import key

from vector import Vector
from ant import Ant, PRO_ANT_IMAGE
from food import Food

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

        self.num_food = 25
        self.num_ants = 15

        self.growFood()

        self.step = 0
        self.generations = 0
        self.population_change_steps = 600

        pyglet.clock.schedule_interval(self.update, 1.0/fps)

        self.ga = ga.RealGeneticAlg(perturbation_bounds = (0.01, 0.3),
                                    crossover_rate = 0.7,
                                    mutation_rate = 0.1
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


    # dt is "delta time" since last update
    def update(self, dt):
        self.step += 1
        for ant in self.ants:
            ant.update(dt, self.food)
            for food in self.food:
                if ant.collidesWith(food):
                    food.eaten = True
                    ant.score += 1

            self.food = filter(lambda f: not f.eaten, self.food)

        self.growFood()

        if self.step > self.population_change_steps:
            self.generations += 1
            scores = map(lambda x: x.score, self.ants)
            print self.generations, min(scores), \
                  max(scores), sum(scores)/float(len(scores))
            #print "Gen: {} Max: {} Avg: {}".format(self.generations,
            #                                       max(scores),
            #                                       sum(scores)/float(len(scores))
            #                                      )

            self.step = 0
            self.updateNets(self.ga.NewPopulation(self.chromosomesFromAnts()))

    def chromosomesFromAnts(self):
        return [Chromosome(a.neural_net.GetWeights(), a.score) for a in self.ants]

    def updateNets(self, chromosomes):
        for i in xrange(len(self.ants)):
            self.ants[i].score = 0
            self.ants[i].updateImage(chromosomes[i].is_top_performer)
            self.ants[i].neural_net.SetWeights(chromosomes[i])

    def getRandomPoint(self, margin = 0):
        return random.randrange(margin ,self.width - margin),random.randrange(margin, self.height - margin)

    def growFood(self):
        #(random.randrange(0,100), random.randrange(0,100))
        while len(self.food) < self.num_food:
            self.food.append(Food(self, self.getRandomPoint(10),
                                  self.sprite_batch))

    def initAnts(self):
        for i in xrange(self.num_ants):
            a = random.randrange(0, 359)
            self.ants.append(Ant(self, self.getRandomPoint(),
                                 Vector(20, a), self.sprite_batch))




if __name__ == "__main__":
    window = SpriteWindow((400,400), fps = 120)
    window.initAnts()
    sys.exit(window.run())
