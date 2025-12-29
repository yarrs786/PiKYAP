import sys


class QuadraticEquationSolver:
    def __init__(self):
        self.a = None
        self.b = None
        self.c = None
        self.x1 = None
        self.x2 = None
        self.x3 = None
        self.x4 = None
        self.d = None

    def get_complex_number_from_args(self, args, index):
        if index < len(args):
            try:
                num = complex(args[index])
                if num.imag == 0:
                    return num
            except ValueError:
                pass
        return None

    def get_complex_number_from_input(self):
        while True:
            try:
                num = complex(input())
                if num.imag == 0:
                    return num
            except ValueError:
                continue

    def get_coefficients(self):
        aflag = 0
        bflag = 0
        cflag = 0
        l = len(sys.argv)

        for i in range(1, l):
            if complex(sys.argv[i]).imag == 0:
                if aflag == 0:
                    self.a = complex(sys.argv[i])
                    aflag = 1
                else:
                    if bflag == 0:
                        self.b = complex(sys.argv[i])
                        bflag = 1
                    else:
                        self.c = complex(sys.argv[i])
                        cflag = 1
                        break

        if self.a is None:
            self.a = self.get_complex_number_from_input()
        if self.b is None:
            self.b = self.get_complex_number_from_input()
        if self.c is None:
            self.c = self.get_complex_number_from_input()

    def calculate_roots(self):
        self.x1 = ((-self.b + (self.b ** 2 - 4 * self.a * self.c) ** 0.5) / (2 * self.a)) ** 0.5
        self.x2 = ((-self.b - (self.b ** 2 - 4 * self.a * self.c) ** 0.5) / (2 * self.a)) ** 0.5
        self.x3 = -((-self.b + (self.b ** 2 - 4 * self.a * self.c) ** 0.5) / (2 * self.a)) ** 0.5
        self.x4 = -((-self.b - (self.b ** 2 - 4 * self.a * self.c) ** 0.5) / (2 * self.a)) ** 0.5

    def calculate_discriminant(self):
        self.d = self.b ** 2 - 4 * self.a * self.c

    def print_discriminant(self):
        print('D =', self.d.real if self.d.imag == 0 else self.d)

    def print_real_roots(self):
        print('Действительные корни:')
        if self.x1.imag == 0:
            print(self.x1.real)
        if self.x2.imag == 0 and self.x1 != self.x2:
            print(self.x2.real)
        if self.x3.imag == 0 and self.x1 != self.x3 and self.x2 != self.x3:
            print(self.x3.real)
        if self.x4.imag == 0 and self.x1 != self.x4 and self.x2 != self.x4 and self.x3 != self.x4:
            print(self.x4.real)

    def solve(self):
        self.get_coefficients()
        self.calculate_roots()
        self.calculate_discriminant()
        self.print_discriminant()
        self.print_real_roots()
        input("Нажмите Enter для выхода")


if __name__ == "__main__":
    solver = QuadraticEquationSolver()
    solver.solve()
