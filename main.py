import random
def sum_event(lst):
    res = 0
    for x in lst:
        if x%2 == 0:
            res += x
    return res


def find_max(lst):
    max = lst[0]
    for x in lst:
        if x > max:
            max = x
    return max


def remove_duplicat(lst):
    new_lst = list(set(lst))
    new_lst.sort()
    return new_lst


def shift_right(lst, k):
    if k <= 0:
        print("Ошибка k>0")
        return
    n = len(lst)
    k %=n
    print(n)
    print("Исходный список:", *lst)
    for i in range(k):
        l_e = lst[-1]
        for j in range(n - 1, 0, -1):
            lst[j] = lst[j - 1]
        lst[0] = l_e
        print(f"Итерация {i}: ", *lst)


def frequency_dict(lst):
    lst.sort()
    res = dict()
    for x in lst:
        res[x] = lst.count(x)
    return res

n = int(input("Введите длину списка: "))
lst = [random.randint(0, 21) for i in range(n)]
print("Иcходный список: ", *lst)
print("Сумма четных элементов списка: ", sum_event(lst))
print("Максимальный элемент списка:  ", max(lst))
new_lst = remove_duplicat(lst)
print("Список с удаленными дублями и отсортированный:    ", *new_lst)
our_dict = frequency_dict(lst)
print("Полученный словарь: ", our_dict)
k = int(input("Введите шаг сдвига k: "))
shift_right(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'x', 'y', 'z', 'w'], k)