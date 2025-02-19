import math

class Student:
    def __init__(self, FIO, marks):
        self.__FIO = FIO
        self.__marks = marks


    @property
    def FIO(self):
        return self.__FIO

    @property
    def marks(self):
        return self.__marks

    def append_marks(self):
        while True:
            try:
                m = list(map(int, input(f"Введите добавляемые оценки студенту {self.FIO}: ").split()))
                for i in range(len(m)):
                    while not (isinstance(m[i], int) and 1 <= m[i] <= 5):
                        print(f"{i}-я оценка неверна. Введите ее заново: ", end = "")
                        while True:
                            try:
                                m[i] = int(input())
                                break
                            except ValueError:
                                print(f"{i}-я оценка не является натуральным числом. Введите ее заново: ", end="")
                break
            except ValueError:
                print(f"Ввод неверный. ", end="")

        self.__marks += m

    def sr_znach(self):
        while len(self.marks) < 2:
            print(f"Количество оценок у студента {self.FIO} должно быть больше или равно 2. Сейчас у него {len(self.marks)} оценок")
            self.append_marks()
        return sum(self.marks)/len(self.marks)

    def get_otklonenie(self):
        M = self.sr_znach()  #выборочное среднее
        db = {x:self.marks.count(x) for x in sorted(self.marks)}
        dispersion_ispravlennay = sum([db[x]*(x-M)**2 for x in db.keys()])/(len(self.marks)-1) #исправленная дисперсия
        return math.sqrt(dispersion_ispravlennay) #стандартное отклонение

    def __repr__(self):
        return f"""------------------------------------------------------
            ФИО: , {self.FIO}
            Список оценок: , {self.marks}
            Средний балл: ", {self.sr_znach()}
            Стандартное отклонение: ", {self.get_otklonenie()}"""

    def mera_razbrosa(self, other):
        if abs(self.sr_znach() - other.sr_znach()) > 10**(-10):
            return f"{self.FIO} и {other.FIO} имеют разный средний балл"
        else:
            if abs(self.get_otklonenie()-other.get_otklonenie()) < 10**(-10):
                return f"{self.FIO} и {other.FIO} имеют одинаковую степень разброса"
            elif self.get_otklonenie() > other.get_otklonenie():
                return f"{self.FIO} имеет большую степень разброса, чем {other.FIO}"
            else:
                return f"{other.FIO} имеет большую степень разброса, чем {self.FIO}"

    @classmethod
    def input(cls, str):
        print(str)
        FIO = input("ФИО = ")
        while True:
            try:
                marks = list(map(int, input(f"Введите оценки студента {FIO}: ").split()))
                for i in range(len(marks)):
                    while not (isinstance(marks[i], int) and 1 <= marks[i] <= 5):
                        print(f"{i}-я оценка неверна. Введите ее заново: ", end = "")
                        while True:
                            try:
                                marks[i] = int(input())
                                break
                            except ValueError:
                                print(f"{i}-я оценка не является натуральным числом. Введите ее заново: ", end="")
                break
            except ValueError:
                print(f"Ввод неверный. ", end="")
        return Student(FIO, marks)



stud1 = Student.input("Заполняем данные о stud1  ")
stud1.append_marks()
stud2 = Student.input("Заполняем данные о stud2")
stud2.append_marks()

res = stud1.mera_razbrosa(stud2)
print(stud1)
print(stud2)
print(res)











