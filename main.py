#!/usr/local/bin/python

# Many thanks to this guy:
# http://www.akeric.com/blog/?p=1527

import sys
import random
import copy

import pyglet
from pyglet.window import key

from vector import Vector
from ant import Ant
from food import Food


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

        self.num_food = 30
        self.num_ants = 10

        self.growFood()

        self.step = 0
        self.population_change_steps = 300

        pyglet.clock.schedule_interval(self.update, 1.0/fps)


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
            #closest = ant.getClosestFood(self.food)
            #ant.vec.angle = (ant.pos - closest).angle
            #if closest.x < ant.pos.x:
            #    ant.vec.angle += 180

            ant.update(dt, self.food)
            for food in self.food:
                if ant.collidesWith(food):
                    food.eaten = True
                    ant.score += 1

            self.food = filter(lambda f: not f.eaten, self.food)

        self.growFood()


    def getRandomPoint(self):
        return random.randrange(0,self.width),random.randrange(0,self.height)


    def growFood(self):
        while len(self.food) < self.num_food:
            self.food.append(Food(self, self.getRandomPoint(),
                                  self.sprite_batch))


    def initAnts(self):
        for i in xrange(10):
            a = random.randrange(0, 359)
            self.ants.append(Ant(self, self.getRandomPoint(),
                                 Vector(20, a), self.sprite_batch))




if __name__ == "__main__":
    window = SpriteWindow((400,400))
    window.initAnts()
    sys.exit(window.run())
