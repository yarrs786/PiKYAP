import unittest
import sys
from io import StringIO
from unittest.mock import patch, Mock
import prog1mod as bq


class TestBiquadraticEquationTDD(unittest.TestCase):
    """TDD тесты для биквадратного уравнения"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.solver = bq.BiquadraticEquationSolver()

    def test_parse_arguments_valid(self):
        """Тест 1: Парсинг корректных аргументов командной строки"""
        # Arrange
        test_args = ["program", "1", "2", "3", "4", "5"]

        # Act
        a, b, c, aflag, bflag, cflag = self.solver.parse_arguments(test_args)

        # Assert
        self.assertEqual(a, complex(1))
        self.assertEqual(b, complex(2))
        self.assertEqual(c, complex(3))
        self.assertEqual(aflag, 1)
        self.assertEqual(bflag, 1)
        self.assertEqual(cflag, 1)

    def test_parse_arguments_insufficient(self):
        """Тест 2: Парсинг недостаточного количества аргументов"""
        # Arrange
        test_args = ["program", "1"]

        # Act
        a, b, c, aflag, bflag, cflag = self.solver.parse_arguments(test_args)

        # Assert
        self.assertEqual(a, complex(1))
        self.assertEqual(b, complex(0))
        self.assertEqual(c, complex(0))
        self.assertEqual(aflag, 1)
        self.assertEqual(bflag, 0)
        self.assertEqual(cflag, 0)

    def test_parse_arguments_complex(self):
        """Тест 3: Парсинг с комплексными числами (должны быть проигнорированы)"""
        # Arrange
        test_args = ["program", "1+2j", "2", "3"]  # Первый аргумент комплексный

        # Act
        a, b, c, aflag, bflag, cflag = self.solver.parse_arguments(test_args)

        # Assert
        self.assertEqual(a, complex(2))  # Должен взять следующий действительный аргумент
        self.assertEqual(b, complex(3))
        self.assertEqual(c, complex(0))

    def test_calculate_discriminant(self):
        """Тест 4: Вычисление дискриминанта"""
        # Arrange
        a, b, c = 1, -3, 2

        # Act
        discriminant = self.solver.calculate_discriminant(a, b, c)

        # Assert
        self.assertEqual(discriminant, 1)
        self.assertEqual(discriminant.imag, 0)

    def test_calculate_roots_simple(self):
        """Тест 5: Вычисление корней для простого уравнения"""
        # Arrange
        a, b, c = 1, 0, -4  # x⁴ - 4 = 0 → x² = ±2 → x = ±√2, ±i√2

        # Act
        x1, x2, x3, x4 = self.solver.calculate_roots(a, b, c)

        # Assert
        # Проверяем, что x3 = -x1 и x4 = -x2
        self.assertAlmostEqual(x3, -x1)
        self.assertAlmostEqual(x4, -x2)

    def test_calculate_roots_quadratic(self):
        """Тест 6: Вычисление корней для уравнения x⁴ - 5x² + 4 = 0"""
        # Arrange
        a, b, c = 1, -5, 4  # Корни: x² = 1 и x² = 4 → x = ±1, ±2

        # Act
        x1, x2, x3, x4 = self.solver.calculate_roots(a, b, c)

        # Assert
        roots = [x1, x2, x3, x4]
        real_roots = [root.real for root in roots if abs(root.imag) < 1e-10]

        # Должны быть 4 действительных корня: ±1, ±2
        self.assertEqual(len(real_roots), 4)

    def test_filter_real_roots(self):
        """Тест 7: Фильтрация действительных корней"""
        # Arrange
        x1, x2, x3, x4 = complex(1, 0), complex(-1, 0), complex(0, 1), complex(0, -1)

        # Act
        real_roots = self.solver.filter_real_roots(x1, x2, x3, x4)

        # Assert
        self.assertEqual(len(real_roots), 2)
        self.assertIn(1.0, real_roots)
        self.assertIn(-1.0, real_roots)

    def test_filter_real_roots_duplicates(self):
        """Тест 8: Фильтрация с дубликатами корней"""
        # Arrange
        x1 = x2 = complex(2, 0)
        x3 = x4 = complex(3, 0)

        # Act
        real_roots = self.solver.filter_real_roots(x1, x2, x3, x4)

        # Assert
        self.assertEqual(len(real_roots), 2)
        self.assertIn(2.0, real_roots)
        self.assertIn(3.0, real_roots)

    def test_filter_real_roots_all_complex(self):
        """Тест 9: Все корни комплексные"""
        # Arrange
        x1, x2, x3, x4 = complex(0, 1), complex(0, -1), complex(1, 1), complex(1, -1)

        # Act
        real_roots = self.solver.filter_real_roots(x1, x2, x3, x4)

        # Assert
        self.assertEqual(len(real_roots), 0)

    def test_format_discriminant_real(self):
        """Тест 10: Форматирование действительного дискриминанта"""
        # Arrange
        d = complex(5, 0)

        # Act
        formatted = self.solver.format_discriminant(d)

        # Assert
        self.assertEqual(formatted, "5.0")

    def test_format_discriminant_complex(self):
        """Тест 11: Форматирование комплексного дискриминанта"""
        # Arrange
        d = complex(3, 4)

        # Act
        formatted = self.solver.format_discriminant(d)

        # Assert
        self.assertEqual(formatted, "(3+4j)")

    def test_solve_full_with_args(self):
        """Тест 12: Полное решение с аргументами командной строки"""
        # Arrange
        test_args = ["program", "1", "0", "-4"]
        mock_input = Mock(side_effect=[])  # Не требуется ввод

        # Act
        d_formatted, real_roots = self.solver.solve_full(test_args, mock_input)

        # Assert
        self.assertEqual(d_formatted, "16.0")
        self.assertEqual(len(real_roots), 2)  # ±√2

    def test_solve_full_without_args(self):
        """Тест 13: Полное решение без аргументов (требует ввода)"""
        # Arrange
        test_args = ["program"]
        mock_input = Mock(side_effect=["1", "0", "-4"])  # Имитируем ввод коэффициентов

        # Act
        d_formatted, real_roots = self.solver.solve_full(test_args, mock_input)

        # Assert
        self.assertEqual(d_formatted, "16.0")
        self.assertEqual(len(real_roots), 2)
        # Проверяем, что mock_input вызывался 3 раза
        self.assertEqual(mock_input.call_count, 3)

    def test_solve_full_partial_args(self):
        """Тест 14: Полное решение с частичными аргументами"""
        # Arrange
        test_args = ["program", "1", "0"]  # Нет коэффициента c
        mock_input = Mock(side_effect=["-4"])  # Вводим только c

        # Act
        d_formatted, real_roots = self.solver.solve_full(test_args, mock_input)

        # Assert
        self.assertEqual(d_formatted, "16.0")
        self.assertEqual(mock_input.call_count, 1)  # Только один запрос ввода


class TestBiquadraticEquationEdgeCasesTDD(unittest.TestCase):
    """TDD тесты для граничных случаев"""

    def setUp(self):
        self.solver = bq.BiquadraticEquationSolver()

    def test_zero_a_coefficient(self):
        """Тест 15: Коэффициент a = 0 (вырожденный случай)"""
        # Arrange
        a, b, c = 0, 1, 1

        # Act & Assert
        with self.assertRaises(ZeroDivisionError):
            self.solver.calculate_roots(a, b, c)

    def test_double_root(self):
        """Тест 16: Уравнение с двукратными корнями x⁴ = 0"""
        # Arrange
        a, b, c = 1, 0, 0

        # Act
        x1, x2, x3, x4 = self.solver.calculate_roots(a, b, c)

        # Assert
        # Все корни должны быть 0 (с учетом погрешности вычислений)
        for root in [x1, x2, x3, x4]:
            self.assertAlmostEqual(abs(root), 0, places=10)

    def test_negative_discriminant(self):
        """Тест 17: Отрицательный дискриминант"""
        # Arrange
        a, b, c = 1, 0, 4  # x⁴ + 4 = 0

        # Act
        discriminant = self.solver.calculate_discriminant(a, b, c)

        # Assert
        self.assertEqual(discriminant, -16)
        self.assertLess(discriminant.real, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
