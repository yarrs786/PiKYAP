import unittest
from rk2 import (
    Row, Table, RowTable,
    create_test_data, create_one_to_many, create_many_to_many,
    task_g1, task_g2, task_g3
)


class TestProgram(unittest.TestCase):

    def setUp(self):
        self.tables, self.rows, self.rows_tables = create_test_data()
        self.one_to_many = create_one_to_many(self.tables, self.rows)
        self.many_to_many = create_many_to_many(self.tables, self.rows, self.rows_tables)

    def test_task_g1(self):
        result = task_g1(self.one_to_many, self.tables)

        expected_tables = ['Аналитические данные', 'Архивные записи', 'Административные таблицы']
        for table_name in expected_tables:
            self.assertIn(table_name, result)

        self.assertEqual(len(result['Аналитические данные']), 3)
        self.assertEqual(result['Аналитические данные'], ['Строка1', 'Строка3', 'Строка6'])
        self.assertEqual(result['Архивные записи'], ['Строка4'])
        self.assertEqual(result['Административные таблицы'], ['Строка5', 'Строка7'])

    def test_task_g2(self):
        result = task_g2(self.one_to_many, self.tables)

        expected_result = [
            ('Административные таблицы', 190),
            ('Сырые данные', 200),
            ('Аналитические данные', 210),
            ('Архивные записи', 220)
        ]

        self.assertEqual(len(result), 4)
        self.assertEqual(result, expected_result)

        sorted_values = [item[1] for item in result]
        self.assertEqual(sorted_values, sorted(sorted_values))

    def test_task_g3(self):
        result = task_g3(self.many_to_many, self.tables)

        expected_keys = ['Административные таблицы', 'Аналитические данные',
                         'Архивные записи', 'Временные данные', 'Сырые данные']

        self.assertEqual(list(result.keys()), sorted(expected_keys))

        self.assertEqual(len(result['Административные таблицы']), 2)
        self.assertEqual(result['Административные таблицы'], ['Строка5', 'Строка7'])
        self.assertEqual(result['Аналитические данные'], ['Строка1', 'Строка3', 'Строка6'])


if __name__ == '__main__':
    unittest.main()
