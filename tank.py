import pyglet as _pyglet
from vector import Vector as _Vector

TANK_IMAGE = "ant.png"

class Tank(_pyglet.sprite.Sprite):
    image = _pyglet.resource.image(TANK_IMAGE)
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

    def __init__(self,parent_window, pos, batch=None):
        super(Tank, self).__init__(Tank.image, pos[0], pos[1], batch=batch)
        self.scale = 0.5
        self.radius = Tank.image.width/2 * self.scale

        self.pos = _Vector(pos[0], pos[1], True)

        self.ltrack = 0
        self.rtrack = 0
        self.rrate = 30

        self.speed = 20
        self.look_vector = _Vector(0, 10)


        self.parent_window = parent_window

        self.score = 0

    def update(self, dt):
        r_rate = (self.rtrack - self.ltrack ) * self.rrate
        self.look_vector.magnitude = (self.rtrack+self.ltrack)/2 * self.speed
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

    def collidesWith(self, obj):
        if (obj.pos-self.pos).magnitude < (obj.radius+self.radius):
            return True
        else:
            return False

    def getClosestFood(self, food):
        closest = None
        for f in food:
            if closest==None or (self.pos-f.pos).magnitude < (self.pos-closest).magnitude:
                closest = f.pos

        return closest
