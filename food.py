import pyglet as _pyglet
from vector import Vector as _Vector

FOOD_IMAGE = "resources/images/food.png"

class Food(_pyglet.sprite.Sprite):
    # Load food image resource
    image = _pyglet.resource.image(FOOD_IMAGE)
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

    def __init__(self,parent_window, pos, batch=None):
        super(Food, self).__init__(Food.image, pos[0], pos[1], batch=batch)
        self.scale = 1
        self.radius = Food.image.width/2 * self.scale

        self.pos = _Vector(pos[0], pos[1], True)
        self.x, self.y = self.pos

        self.parent_window = parent_window
        self.eaten = False

    def update(self, dt):
        pass

    def collidesWith(self, ant):
        if (ant.pos-self.pos).magnitude < (ant.radius+self.radius):
            return True
        else:
            return False
