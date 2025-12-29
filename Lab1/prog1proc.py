import sys


def get_complex_number_from_args(args, index):
    if index < len(args):
        try:
            num = complex(args[index])
            if num.imag == 0:
                return num
        except ValueError:
            pass
    return None


def get_complex_number_from_input():
    while True:
        try:
            num = complex(input())
            if num.imag == 0:
                return num
        except ValueError:
            continue


def get_coefficients():
    coefficients = {}

    aflag = 0
    bflag = 0
    cflag = 0
    l = len(sys.argv)

    for i in range(1, l):
        if complex(sys.argv[i]).imag == 0:
            if aflag == 0:
                coefficients['a'] = complex(sys.argv[i])
                aflag = 1
            else:
                if bflag == 0:
                    coefficients['b'] = complex(sys.argv[i])
                    bflag = 1
                else:
                    coefficients['c'] = complex(sys.argv[i])
                    cflag = 1
                    break

    if 'a' not in coefficients:
        coefficients['a'] = get_complex_number_from_input()
    if 'b' not in coefficients:
        coefficients['b'] = get_complex_number_from_input()
    if 'c' not in coefficients:
        coefficients['c'] = get_complex_number_from_input()

    return coefficients['a'], coefficients['b'], coefficients['c']


def calculate_roots(a, b, c):
    x1 = ((-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)) ** 0.5
    x2 = ((-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)) ** 0.5
    x3 = -((-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)) ** 0.5
    x4 = -((-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)) ** 0.5

    return x1, x2, x3, x4


def print_discriminant(a, b, c):
    d = b ** 2 - 4 * a * c
    print('D =', d.real if d.imag == 0 else d)


def print_real_roots(x1, x2, x3, x4):
    print('Действительные корни:')
    if x1.imag == 0:
        print(x1.real)
    if x2.imag == 0 and x1 != x2:
        print(x2.real)
    if x3.imag == 0 and x1 != x3 and x2 != x3:
        print(x3.real)
    if x4.imag == 0 and x1 != x4 and x2 != x4 and x3 != x4:
        print(x4.real)


def main():
    a, b, c = get_coefficients()

    x1, x2, x3, x4 = calculate_roots(a, b, c)

    print_discriminant(a, b, c)
    print_real_roots(x1, x2, x3, x4)

    input("Нажмите Enter для выхода")


if __name__ == "__main__":
    main()
