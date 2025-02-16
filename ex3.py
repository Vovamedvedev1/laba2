import math
import random
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
from ex2 import Point


class Circule():
    def __init__(self, center, radius):
        self.__center = center
        if not (isinstance(radius, int) or isinstance(radius, float)):
            raise ValueError("Радиус окружности может принимать только численные значения")
        if radius <= 0:
            raise ValueError("Радиус окружности должен быть положителльным числом")
        self.__radius = radius

    @property
    def center(self):
        return self.__center

    @property
    def radius(self):
        return self.__radius

    def calcLen(self):
        return math.pi*2*self.radius

    def calcArea(self):
        return math.pi*self.radius**2

    def isPeresekautsa(self, other):
        res = f"Окружности (x{'-'+str(self.center.x) if self.center.x>=0 else '+'+str(abs(self.center.x))})^2+(y{'-'+str(self.center.y) if self.center.y>=0 else '+'+str(abs(self.center.y))})^2={self.radius**2} и (x{'-'+str(other.center.x) if other.center.x>=0 else '+'+str(abs(other.center.x))})^2+(y{'-'+str(other.center.y) if other.center.y>=0 else '+'+str(abs(other.center.y))})^2={other.radius**2}"
        res_points = []
        d = self.center.distanse(other.center)
        if (d - self.radius - other.radius) > 10**(-10):
            res += " - не пересекаются"
        elif (abs(self.radius-other.radius) - d) > 10**(-10):
            res += " - не пересекаются и одна окружность вложена в другую"
        elif abs(d) < 10**(-10) and abs(self.radius-other.radius) < 10**(-10):
            res += " - совпадают"
        else:
            a = (self.radius**2 - other.radius**2 + d**2) / (2 * d)
            h = math.sqrt(self.radius**2 - a**2)
            x0 = self.center.x + a * (other.center.x - self.center.x) / d
            y0 = self.center.y + a * (other.center.y - self.center.y) / d
            x_intersect1 = x0 + h * (other.center.y - self.center.y) / d
            y_intersect1 = y0 - h * (other.center.x - self.center.x) / d
            x_intersect2 = x0 - h * (other.center.y - self.center.y) / d
            y_intersect2 = y0 + h * (other.center.x - self.center.x) / d
            if abs(d - self.radius - other.radius) < 10**(-10) or abs(d - abs(self.radius - other.radius)) < 10**(-10):
                res_points.append(Point(x_intersect1, y_intersect1))
                res += f" - пересекаются в одной точке с координатами {res_points[0]}"
            else:
                res_points.append(Point(x_intersect1, y_intersect1))
                res_points.append(Point(x_intersect2, y_intersect2))
                res += f" - пересекаются в двух точках с координатами {res_points[0]}, {res_points[1]}"
        print(res)
        return res_points

    def __repr__(self):
        return f"""Уравнение окружности: (x{'-'+str(self.center.x) if self.center.x>=0 else '+'+str(abs(self.center.x))})^2+(y{'-'+str(self.center.y) if self.center.y>=0 else '+'+str(abs(self.center.y))})^2={self.radius**2}
        Центр окружности: {self.center}
        Радиус окружности: {self.radius}
        Длина окружности: {self.calcLen()}
        Площадь круга: {self.calcArea()}"""

    @classmethod
    def input(cls, str):
        print(str, end="")
        while True:
            try:
                lst = list(map(float, input().split()))
                if len(lst) != 3:
                    print(f"Должно быть введно 3 аргумента, а вы ввели {len(lst)}. Введите аргументы заново: ", end = "")
                    continue
                x, y, radius = lst
                while radius <= 0:
                    print(f"Радиус должен быть положительным. Введите радиус заново: ", end="")
                    radius = float(input())
                break
            except ValueError:
                print("Ввод некорректен. Введите аргументы заново: ", end = "")
        return Circule(Point(x, y), radius)

    def draw(self, ax, clr, lbl):
        circle = plt.Circle((self.center.x, self.center.y), self.radius, color=clr, fill=False, label=lbl, linewidth=5)
        ax.add_patch(circle)


def drawCirculsPoints(circuls, points_peresech):
    fig, ax = plt.subplots(figsize=(24, 16))
    colors = []
    colors_massive = list(clrs.TABLEAU_COLORS.values())
    for i, x in enumerate(circuls):
        color = random.choice(colors_massive)
        while color in colors:
            color = random.choice(colors_massive)
        colors.append(color)
        x.draw(ax, color, f"cir{i}")
    ax.scatter([t.x for t in points_peresech], [t.y for t in points_peresech], color="red", marker="s")
    for t in points_peresech:
        plt.annotate(f"({round(t.x,3)}, {round(t.y,3)})", (t.x, t.y), textcoords='offset points', xytext=(5, 5), ha='left', va='bottom', arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Примеры окружностей')
    ax.axis('equal')
    plt.legend()
    plt.grid(True)
    plt.show()


circuls = []
points_peresech = []
n = int(input("Введите число окружностей:  "))
for i in range(n):
    x = Circule.input(f"Введите через пробел координаты центра и радиус окружности cir{i} = ")
    circuls.append(x)
    print(f"cir{i} = ", circuls[i])

for i in range(n):
    for j in range(i+1, n):
        pt = circuls[i].isPeresekautsa(circuls[j])
        points_peresech += pt

drawCirculsPoints(circuls, points_peresech)



