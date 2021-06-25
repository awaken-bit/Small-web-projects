def sort_quick(lis):       # Быстрая сортировка
    if len(lis) <= 1:
        return lis
    else:
        q = choice(lis)   # Опорный элемент
    l_nums = [n for n in lis if n < q]   # Числа меньше опорного элемента
    e_nums = [q] * lis.count(q)   # Числа равные опорному числу
    b_nums = [n for n in lis if n > q]   # Числа больше опорного числа

    return sort_quick(l_nums) + e_nums + sort_quick(b_nums)