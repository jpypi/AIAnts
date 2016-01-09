import pyglet as _pyglet

from vector import Vector as _Vector
from ffnn.neuralnet import NeuralNet as _NeuralNet

ANT_IMAGE = "resources/images/ant.png"
PRO_ANT_IMAGE = "resources/images/ant-good.png"

class Ant(_pyglet.sprite.Sprite):
    image = _pyglet.image.load(ANT_IMAGE)
    pro_image = _pyglet.image.load(PRO_ANT_IMAGE)
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

    def __init__(self, parent_window, pos, move_vec, batch=None):
        super(Ant, self).__init__(Ant.image, pos[0], pos[1], batch=batch)
        self.parent_window = parent_window

        self.scale = 0.4
        self.radius = Ant.image.width/2 * self.scale

        self.look_vector = move_vec
        self.pos = _Vector(pos[0], pos[1], True)

        self.speed = 5
        self.rrate = 40

        self.neural_net = _NeuralNet(6, 2, [8, 6])
        self.score = 0

    def updateImage(self, is_pro):
        if is_pro:
            self.image = Ant.pro_image
        else:
            self.image = Ant.image

    def update(self, dt, food, poison):
        closest_food = self.getClosestConsumableVec(food);
        closest_poison = self.getClosestConsumableVec(poison);

        ltrack, rtrack = self.neural_net.GetOutput((self.look_vector.x,
                                                    self.look_vector.y,
                                                    closest_food.x,
                                                    closest_food.y,
                                                    closest_poison.x,
                                                    closest_poison.y
                                                    ))



        r_rate = (rtrack - ltrack ) * self.rrate
        self.look_vector.magnitude = (rtrack + ltrack) / 2 * self.speed
        self.look_vector.angle += r_rate

        self.rotation = 90 - self.look_vector.angle

        self.pos[0] += self.look_vector[0] * dt
        self.pos[1] += self.look_vector[1] * dt
        self.x = self.pos.x
        self.y = self.pos.y

        # Clamping/wrapping
        if self.pos.x > self.parent_window.width: self.pos.x = 0
        if self.pos.x < 0: self.pos.x = self.parent_window.width
        if self.pos.y > self.parent_window.height: self.pos.y = 0
        if self.pos.y < 0: self.pos.y = self.parent_window.height


    def collidesWith(self, other_ant):
        if (other_ant.pos-self.pos).magnitude < (other_ant.radius+self.radius):
            return True
        else:
            return False


    def getClosestFood(self, food):
        closest = None
        for f in food:
            if closest == None or \
               (self.pos - f.pos).magnitude < (self.pos-closest).magnitude:
                closest = f.pos

        return closest


    def getClosestConsumableVec(self, food):
        closest = None
        for f in food:
            if closest == None or (self.pos-f.pos).magnitude < closest.magnitude:
                closest = self.pos-f.pos

        return closest
