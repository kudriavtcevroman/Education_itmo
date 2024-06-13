# ТЕМПЕРАТУРНЫЕ ИЗМЕРЕНИЯ

lst = [-1, 2, 56, -456, None, 43, None, -43, -8, None, 374, 74, -20, None]
lst_2 = [2, 4, None, -2, -4, None, 1]
def arg(lst: list):
    volume = ([], [])
    for num in lst:
        if num == None:
            continue
        else:
            if int(num) >= 0:
                volume[1].append(int(num))
            else:
                volume[0].append(int(num))
    volume[0].sort(reverse=True)
    volume[1].sort()
    return volume
print(arg(lst))
print(arg(lst_2))



# ВОЗВЕДЕНИЕ ЧИСЛА В СТЕПЕНЬ

lst_sq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
num = 5
degree = 3

# ОБЫЧНОЕ ВОЗВЕДЕНИЕ В СТЕПЕНЬ

def sqrt_num(x, d):
    x = pow(x, d)
    return x
print(sqrt_num(num, degree))

# РЕКУРСИВНОЕ ВОЗВЕДЕНИЕ В СТЕПЕНЬ

def sqrt_r(lst: list, d):
    lst_sqrt = list()
    def sqrt_n(x, d):
        x = pow(x, d)
        return x
    for k in lst:
        lst_sqrt.append(sqrt_n(k, d))
    return lst_sqrt
print(sqrt_r(lst_sq, degree))

