from django import template

register = template.Library()


@register.filter()
def text_by_point(number):
    """Metodo que se utiliza para determinar si el numero es divisible por la cantidad.

    """
    number_str = str(number)
    invert_num = number_str[::-1]
    list_check = list(invert_num)
    length = len(list_check)
    count = 0
    for i in range(3, length, 3):
        list_check.insert(i + count, '.')
        count += 1
    result = ''
    for x in list_check[::-1]:
        result += x
    return result
