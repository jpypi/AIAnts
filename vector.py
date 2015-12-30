import math

class Vector(object):
    def __init__(self, x_mag, y_ang, is_cartesian = False):
        # Setting the literal attributes underlying the properties
        # here should technically be more efficient (fewer calls to
        # __update* methods
        if is_cartesian:
            self.__x = float(x_mag)
            self.__y = float(y_ang)
            self.__updateVector()
        else:
            self.__magnitude = float(x_mag)
            self.__angle = math.radians(float(y_ang))
            self.__updatePoint()

    def __updateVector(self):
        if self.__x == 0:
            self.__angle = 0
        else:
            self.__angle = math.atan(self.__y / self.__x)
        self.__magnitude = math.sqrt(self.__x**2 + self.__y**2)

    def __updatePoint(self):
        self.__x = math.cos(self.__angle) * self.__magnitude
        self.__y = math.sin(self.__angle) * self.__magnitude

    # Angle is stored in radians and converted at io
    @property
    def angle(self):
        return math.degrees(self.__angle)
    @angle.setter
    def angle(self, value):
        self.__angle = math.radians(float(value))
        self.__updatePoint()

    @property
    def magnitude(self):
        return self.__magnitude
    @magnitude.setter
    def magnitude(self, value):
        self.__magnitude = float(value)
        self.__updatePoint()

    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self, value):
        self.__x = float(value)
        self.__updateVector()

    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self, value):
        self.__y = float(value)
        self.__updateVector()

    def __div__(self, value):
        self.__magnitude /= float(value)
        self.__updateVector()

    def __mul__(self, value):
        self.__magnitude *= value
        self.__updatePoint()

    def __repr__(self):
        return "({},{}) aka {} at {} deg".format(self.x, self.y,
                                                 self.magnitude,
                                                 self.angle)

    def __len__(self):
        return 2

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError, "Vector only has indicies 0 and 1 for x and y!"

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError, "Vector only has indicies 0 and 1 for x and y!"

    def __add__(self, vec2):
        return Vector(self.x + vec2.x, self.y + vec2.y, True)

    def __sub__(self, vec2):
        return Vector(self.x - vec2.x, self.y - vec2.y, True)

origin = Vector(0,0)
