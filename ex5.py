from prettytable import PrettyTable

class Matrix():
    def __init__(self, n, m, matr):
        self.__n = n
        self.__m = m
        self.__matr = matr

    @property
    def n(self):
        return self.__n

    @property
    def m(self):
        return self.__m

    @property
    def matr(self):
        return self.__matr

    def __add__(self, other):
        if self.n != other.n or self.m != other.m:
            raise ArithmeticError("Правый и левый операнд должны быть одинаковой размерности")
        a = [[self.matr[i][j] + other.matr[i][j] for j in range(self.m)] for i in range(self.n)]
        return Matrix(self.n, self.m, a)

    def __sub__(self, other):
        if self.n != other.n or self.m != other.m:
            raise ArithmeticError("Правый и левый операнд должны быть одинаковой размерности")
        a = [[self.matr[i][j] - other.matr[i][j] for j in range(self.m)] for i in range(self.n)]
        return Matrix(self.n, self.m, a)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            a = [[self.matr[i][j]*other for j in range(self.m)] for i in range(self.n)]
            return Matrix(self.n, self.m, a)
        else:
            if self.m != other.n:
                raise ArithmeticError("Матрицы должны удовлетворять условию [x][m]*[m][b]")
            a = [[0 for j in range(other.m)] for i in range(self.n)]
            for i in range(self.n):
                for j in range(other.m):
                    for k in range(self.m):
                        a[i][j] += self.matr[i][k]*other.matr[k][j]
            return Matrix(self.n, other.m, a)

    def transpone(self):
        b = [[self.matr[j][i] for j in range(self.n)] for i in range(self.m)]
        return Matrix(self.m, self.n, b)

    def lup_decomposition(self):
        if self.n != self.m:
            raise ValueError("Матрица не является квадратной")
        N = self.n
        A = [x[:] for x in self.matr]
        P = [[1 if i==j else 0 for j in range(N)]for i in range(N)]
        count_permutation = 0
        for i in range(N):
            leader_index = i
            max_value = abs(A[i][i])
            for k in range(i+1,N):
                if abs(A[k][i]) > max_value:
                    max_value = abs(A[k][i])
                    leader_index = k
            if abs(A[leader_index][i]) < 10**(-10):
                raise ArithmeticError("Матрица вырожденная")
            if leader_index != i:
                A[i], A[leader_index] = A[leader_index], A[i]
                P[i], P[leader_index] = P[leader_index], P[i]
                count_permutation+=1
            for j in range(i + 1, N):
                factor = A[j][i] / A[i][i]
                A[j][i] = factor
                for k in range(i + 1, N):
                    A[j][k] -= factor * A[i][k]
        L = [[0.0] * N for _ in range(N)]
        U = [[0.0] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if i > j:
                    L[i][j] = A[i][j]
                elif i == j:
                    L[i][j] = 1.0
                    U[i][j] = A[i][j]
                else:
                    U[i][j] = A[i][j]
        return (L,U,P,count_permutation)

    def getDeterminant(self):
        try:
            L,U,P,count_permutation = self.lup_decomposition()
        except ArithmeticError:
            return 0.0
        prouzv = 1
        for i in range(self.n):
            prouzv*=U[i][i]
        return ((-1)**count_permutation)*prouzv

    def calcSLAU(self, other):
        if other.n != self.n:
            raise ValueError("Неверная размерность вектор-столбца b")
        L, U, P, count_permutation = self.lup_decomposition()
        if L is None or U is None or P is None:
            raise ValueError("Матрица A вырождена, решение не существует")
        Pb = [[0.0 for i in range(other.m)] for j in range(other.n)]
        for k in range(other.m):
            for i in range(other.n):
                for j in range(other.n):
                    if P[i][j] == 1.0:
                        Pb[i][k] = other.matr[j][k]
                        break
        y = [[0.0 for i in range(other.m)] for j in range(len(L))]
        for k in range(other.m):
            for i in range(len(L)):
                y[i][k] = Pb[i][k]
                for j in range(i):
                    y[i][k] -= L[i][j] * y[j][k]
        x = Matrix(len(U), other.m, [[0.0 for j in range(other.m)] for i in range(len(U))])
        for k in range(other.m):
            for i in range(len(U) - 1, -1, -1):
                x.matr[i][k] = y[i][k]
                for j in range(i + 1, len(U)):
                    x.matr[i][k] -= U[i][j] * x.matr[j][k]
                x.matr[i][k] /= U[i][i]
        return x

    def __pow__(self, power, modulo=None):
        if not isinstance(power, int):
            raise ArithmeticError("Показателем степени должно быть число типа int большее или равное -1 и не равное 0")
        if power < -1 or power == 0:
            raise ArithmeticError("Показателем степени должно быть число типа int большее или равное -1 и не равное 0")
        if power == -1:
            if self.n != self.m:
                raise ValueError("Обращать можно только квадратную матрицу")
            res = self.calcSLAU(Matrix(self.n, self.n, [[1 if i == j else 0 for j in range(self.n)] for i in range(self.n)]))
        else:
            if self.n != self.m:
                raise ArithmeticError("Возводить в степень можно только квадратную матрицу")
            res = self
            i = power-1
            while i > 0:
                res = res * self
                i-=1
        return res

    def __repr__(self):
        table = PrettyTable([])
        table.hrules = True
        table.align = "r"
        table.border = True
        table.header = False
        for x in self.matr:
            table.add_row([round(t,8) for t in x])
        return str(table)

    @classmethod
    def input(cls, s):
        print(s)
        while True:
            try:
                rows = int(input("Введите количество строк: "))
                cols = int(input("Введите количество столбцов: "))
                if rows <= 0:
                    print("Количество строк должно быть положительным.")
                    continue
                if cols <= 0:
                    print("Количество столбцов должно быть положительным.")
                    continue
                break
            except ValueError:
                print(
                    "Ошибка(неадекватная размерность матрицы): Введите целые положительные числа для количества строк и столбцов.")
        matr = [[0.0] * cols for i in range(rows)]
        for i in range(rows):
            while True:
                try:
                    lst = list(map(float, input(f"Введите {i}-ю строку матрицы: ").split()))
                    if len(lst) != cols:
                        print(
                            f"Ошибка. {i}-я строка должна содержать {cols} элементов, но вы ввели {len(lst)} элементов. Необходимо ввести строку снова.")
                        continue
                    matr[i] = lst
                    break
                except ValueError:
                    print(
                        f"Ошибка. Элементы в {i}-ой строке должны быть разделены пробелами и являться числами. Необходимо ввести строку снова.")
        return Matrix(rows, cols, matr)


try:
    A = Matrix.input("A = ")
    print("A = \n", A)
    detA = A.getDeterminant()
    print("Определитель матрицы A: ", detA)
    AA = A**(-1)
    print("Обратная матрицы A: \n", AA)
    proverka = AA * A
    print("Проверка A * AA: \n", proverka)
except Exception as e:
    print(str(e))

try:
    B = Matrix.input("B = ")
    print("B = \n", B)
    detB = B.getDeterminant()
    print("Определитель матрицы B: ", detB)
    BB = B ** (-1)
    print("Обратная матрицы B: \n", BB)
    proverka = BB * B
    print("Проверка BB * B: \n", proverka)
except Exception as e:
    print(str(e))

try:
    C = Matrix.input("C = ")
    print("C = \n", C)
    detC = C.getDeterminant()
    print("Определитель матрицы C: ", detC)
    CC = C ** (-1)
    print("Обратная матрицы C: \n", CC)
    proverka = CC * C
    print("Проверка C * CC: \n", proverka)
except Exception as e:
    print(str(e))


try:
    D = Matrix.input("D = ")
    print("D = \n", D)
    detD = D.getDeterminant()
    print("Определитель матрицы D: ", detD)
    DD = D ** (-1)
    print("Обратная матрицы D: \n", DD)
    proverka = DD * D
    print("Проверка DD * D \n", proverka)
except Exception as e:
    print(str(e))

try:
    res1 = ((A*B+C*D)*D.transpone()*(-0.5))**(-1)
    print("Арифметическое выражение ((A*B+C*D)*D.transpone()*(-0.5))**(-1) = \n", res1)
except Exception as e:
    print(str(e))

try:
    res2 = (((B.transpone()*(A.transpone()*D-B*C)*D**(-1))*(-6))**(-1))*10**(-11)
    print("Арифметическое выражение (((B.transpone()*(A.transpone()*D-B*C)*D**(-1))*(-6))**(-1))*10**(-11) = \n", res2)
except Exception as e:
    print(str(e))

try:
    res3 = ((((A*B-C*D)*C**(-1))**3)**(-1)).transpone()*10**5
    print("Арифметическое выражение ((((A*B-C*D)*C**(-1))**3)**(-1)).transpone()*10**5 = \n", res3)
except Exception as e:
    print(str(e))

try:
    print("Решение СЛАУ")
    b = Matrix.input("Введите вектор чтолбец b")
    x = C.calcSLAU(b)
    print("Решение СЛАУ Cx = b:   \n", x)
    print("Проверка Cx-b: \n", C*x-b)
except Exception as e:
    print(str(e))