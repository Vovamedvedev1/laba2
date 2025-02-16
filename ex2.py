import math

class Point():
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def distanse(self, other):
        return math.sqrt((other.x-self.x)**2 + (other.y-self.y)**2)

    def midpoint(self, other):
        X = (self.x + other.x) / 2
        Y = (self.y + other.y) / 2
        return Point(X,Y)

    def isLine(self, pt2, pt3):
        res = ""
        if abs((self.x - pt2.x)*(pt3.y - pt2.y) - (self.y - pt2.y)*(pt3.x - pt2.x)) < 10**(-10):
            res = "лежат"
        else:
            res = "не лежат"
        return f"Точки {self}; {pt2}; {pt3} - {res} на одной прямой"

    def __eq__(self, other):
        return bool(abs(self.x - other.x) < 10**(-10) and abs(self.y - other.y) < 10**(-10))

    def __repr__(self):
        return f"({round(self.x,8)}, {round(self.y,8)})"


pt1 = Point(-0.75, -1.5)
pt2 = Point(0.5, 1)
pt3 = Point(-1.25, -2.5)

print(f"Расстояние от точки {pt1} до точки {pt2}  =  {round(pt1.distanse(pt2), 3)}")
print(f"Расстояние от точки {pt1} до точки {pt3}  =  {round(pt1.distanse(pt3), 3)}")
print(f"Расстояние от точки {pt2} до точки {pt1}  =  {round(pt2.distanse(pt1), 3)}")
print(f"Расстояние от точки {pt2} до точки {pt3}  =  {round(pt2.distanse(pt3), 3)}")

print(f"Координаты центра отрезка {pt1} -> {pt2}  = {pt1.midpoint(pt2)}")
print(f"Координаты центра отрезка {pt1} -> {pt3}  = {pt1.midpoint(pt3)}")
print(f"Координаты центра отрезка {pt2} -> {pt1} = {pt2.midpoint(pt1)}")
print(f"Координаты центра отрезка {pt2} -> {pt3}  = {pt2.midpoint(pt3)}")

print(pt1.isLine(pt2,pt3))
pt4 = Point(1,1)
print(pt1.isLine(pt4,pt3))
