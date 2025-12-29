import sys
from typing import List, Tuple, Optional


class BiquadraticEquationSolver:
    """Класс для решения биквадратных уравнений вида ax⁴ + bx² + c = 0"""

    @staticmethod
    def parse_arguments(args: List[str]) -> Tuple[complex, complex, complex]:
        """
        Парсит аргументы командной строки для получения коэффициентов a, b, c.
        Возвращает кортеж из трех комплексных чисел (a, b, c).
        """
        aflag = bflag = cflag = 0
        a = b = c = 0j

        l = len(args)
        for i in range(1, l):
            try:
                num = complex(args[i])
                if num.imag == 0:  # Только действительные числа
                    if aflag == 0:
                        a = num
                        aflag = 1
                    elif bflag == 0:
                        b = num
                        bflag = 1
                    elif cflag == 0:
                        c = num
                        cflag = 1
                        break
            except ValueError:
                continue  # Пропускаем некорректные аргументы

        return a, b, c, aflag, bflag, cflag

    @staticmethod
    def get_missing_coefficients(aflag: int, bflag: int, cflag: int,
                                 input_func=input) -> Tuple[complex, complex, complex]:
        """
        Запрашивает недостающие коэффициенты у пользователя.
        input_func можно заменить на мок в тестах.
        """
        a = b = c = 0j

        if aflag == 0:
            a = BiquadraticEquationSolver._get_real_input("Введите коэффициент a: ", input_func)
        else:
            a = None  # Будет установлено позже

        if bflag == 0:
            b = BiquadraticEquationSolver._get_real_input("Введите коэффициент b: ", input_func)
        else:
            b = None

        if cflag == 0:
            c = BiquadraticEquationSolver._get_real_input("Введите коэффициент c: ", input_func)
        else:
            c = None

        return a, b, c

    @staticmethod
    def _get_real_input(prompt: str, input_func) -> complex:
        """Получает действительное число от пользователя"""
        while True:
            try:
                x = complex(input_func(prompt))
                if x.imag == 0:
                    return x
                print("Пожалуйста, введите действительное число!")
            except (ValueError, EOFError):
                print("Некорректный ввод. Попробуйте снова.")

    @staticmethod
    def calculate_discriminant(a: complex, b: complex, c: complex) -> complex:
        """Вычисляет дискриминант квадратного уравнения относительно x²"""
        return b ** 2 - 4 * a * c

    @staticmethod
    def calculate_roots(a: complex, b: complex, c: complex) -> Tuple[complex, complex, complex, complex]:
        """
        Вычисляет все 4 корня биквадратного уравнения.
        Формулы соответствуют исходному коду.
        """
        # Вычисляем дискриминант для подстановки в формулы
        discriminant = b ** 2 - 4 * a * c
        sqrt_discriminant = discriminant ** 0.5

        # Вычисляем корни по формулам из исходного кода
        x1 = ((-b + sqrt_discriminant) / (2 * a)) ** 0.5
        x2 = ((-b - sqrt_discriminant) / (2 * a)) ** 0.5
        x3 = -x1
        x4 = -x2

        return x1, x2, x3, x4

    @staticmethod
    def filter_real_roots(x1: complex, x2: complex, x3: complex, x4: complex) -> List[float]:
        """
        Фильтрует действительные корни, убирая дубликаты.
        Возвращает список уникальных действительных корней.
        """
        real_roots = []

        # Проверяем каждый корень и добавляем только уникальные действительные
        roots = [x1, x2, x3, x4]
        seen_roots = set()

        for root in roots:
            if abs(root.imag) < 1e-10:  # Учитываем погрешность вычислений
                real_part = root.real
                # Округляем для избежания проблем с плавающей точкой
                rounded_real = round(real_part, 10)
                if rounded_real not in seen_roots:
                    seen_roots.add(rounded_real)
                    real_roots.append(real_part)

        return real_roots

    @staticmethod
    def format_discriminant(d: complex) -> str:
        """Форматирует дискриминант для вывода"""
        if d.imag == 0:
            return str(d.real)
        else:
            return str(d)

    @staticmethod
    def solve_full(args: List[str], input_func=input) -> Tuple[str, List[float]]:
        """
        Полное решение уравнения: парсинг, вычисление, фильтрация.
        Возвращает отформатированный дискриминант и список действительных корней.
        """
        # Парсим аргументы
        a, b, c, aflag, bflag, cflag = BiquadraticEquationSolver.parse_arguments(args)

        # Получаем недостающие коэффициенты
        missing_a, missing_b, missing_c = BiquadraticEquationSolver.get_missing_coefficients(
            aflag, bflag, cflag, input_func
        )

        # Объединяем коэффициенты
        if aflag == 0:
            a = missing_a
        if bflag == 0:
            b = missing_b
        if cflag == 0:
            c = missing_c

        # Вычисляем дискриминант
        d = BiquadraticEquationSolver.calculate_discriminant(a, b, c)
        d_formatted = BiquadraticEquationSolver.format_discriminant(d)

        # Вычисляем корни
        x1, x2, x3, x4 = BiquadraticEquationSolver.calculate_roots(a, b, c)

        # Фильтруем действительные корни
        real_roots = BiquadraticEquationSolver.filter_real_roots(x1, x2, x3, x4)

        return d_formatted, real_roots


def main():
    """Основная функция для запуска из командной строки"""
    solver = BiquadraticEquationSolver()

    # Получаем результат решения
    d_formatted, real_roots = solver.solve_full(sys.argv)

    # Выводим результаты
    print('D =', d_formatted)
    print('Действительные корни:')
    if real_roots:
        for root in real_roots:
            print(root)
    else:
        print("Действительных корней нет")

    input("Нажмите Enter для выхода")


if __name__ == "__main__":
    main()
