using System;
using System.Numerics;

class Program
{
    static void Main(string[] args)
    {
        Complex a = Complex.Zero;
        Complex b = Complex.Zero;
        Complex c = Complex.Zero;
        bool aflag = false, bflag = false, cflag = false;
        
        // Обработка аргументов командной строки
        for (int i = 0; i < args.Length; i++)
        {
            if (TryParseRealComplex(args[i], out Complex value))
            {
                if (!aflag)
                {
                    a = value;
                    aflag = true;
                }
                else if (!bflag)
                {
                    b = value;
                    bflag = true;
                }
                else if (!cflag)
                {
                    c = value;
                    cflag = true;
                    break;
                }
            }
        }
        
        // Ввод недостающих коэффициентов
        if (!aflag)
        {
            a = ReadRealComplexFromConsole("Введите a: ");
        }
        if (!bflag)
        {
            b = ReadRealComplexFromConsole("Введите b: ");
        }
        if (!cflag)
        {
            c = ReadRealComplexFromConsole("Введите c: ");
        }
        
        // Вычисление корней (сохранены оригинальные формулы)
        Complex discriminant = b * b - 4 * a * c;
        Complex x1 = Complex.Pow((-b + Complex.Pow(b * b - 4 * a * c, 2)) / (2 * a), 0.5);
        Complex x2 = Complex.Pow((-b - Complex.Pow(b * b - 4 * a * c, 2)) / (2 * a), 0.5);
        Complex x3 = -Complex.Pow((-b + Complex.Pow(b * b - 4 * a * c, 2)) / (2 * a), 0.5);
        Complex x4 = -Complex.Pow((-b - Complex.Pow(b * b - 4 * a * c, 2)) / (2 * a), 0.5);
        
        // Вывод дискриминанта
        Console.Write("D = ");
        if (discriminant.Imaginary == 0)
            Console.WriteLine(discriminant.Real);
        else
            Console.WriteLine("(" + discriminant.Real + ", " + discriminant.Imaginary + ")");
        
        // Вывод действительных корней
        Console.WriteLine("Действительные корни:");
        if (Math.Abs(x1.Imaginary) < 1e-10)
            Console.WriteLine(x1.Real);
        if (Math.Abs(x2.Imaginary) < 1e-10 && !ComplexEquals(x1, x2))
            Console.WriteLine(x2.Real);
        if (Math.Abs(x3.Imaginary) < 1e-10 && !ComplexEquals(x1, x3) && !ComplexEquals(x2, x3))
            Console.WriteLine(x3.Real);
        if (Math.Abs(x4.Imaginary) < 1e-10 && !ComplexEquals(x1, x4) && !ComplexEquals(x2, x4) && !ComplexEquals(x3, x4))
            Console.WriteLine(x4.Real);
        
        Console.WriteLine("Нажмите Enter для выхода");
        Console.ReadLine();
    }
    
    // Метод для парсинга действительного комплексного числа из строки
    static bool TryParseRealComplex(string input, out Complex result)
    {
        result = Complex.Zero;
        
        if (string.IsNullOrWhiteSpace(input))
            return false;
        
        // Пробуем распарсить как double (действительное число)
        if (double.TryParse(input, out double realValue))
        {
            result = new Complex(realValue, 0);
            return true;
        }
        
        // Пробуем распарсить комплексное число в формате (real, imaginary)
        input = input.Trim();
        if (input.StartsWith("(") && input.EndsWith(")"))
        {
            string content = input.Substring(1, input.Length - 2);
            string[] parts = content.Split(',');
            
            if (parts.Length == 2 && 
                double.TryParse(parts[0].Trim(), out double real) &&
                double.TryParse(parts[1].Trim(), out double imag))
            {
                result = new Complex(real, imag);
                // Проверяем, что мнимая часть равна 0 (как в оригинальном коде)
                return Math.Abs(imag) < 1e-10;
            }
        }
        
        return false;
    }
    
    // Метод для ввода комплексного числа с нулевой мнимой частью из консоли
    static Complex ReadRealComplexFromConsole(string prompt)
    {
        while (true)
        {
            Console.Write(prompt);
            string input = Console.ReadLine();
            
            if (TryParseRealComplex(input, out Complex result))
                return result;
            
            Console.WriteLine("Ошибка: введите действительное число!");
        }
    }
    
    // Метод для сравнения комплексных чисел с учетом погрешности
    static bool ComplexEquals(Complex a, Complex b)
    {
        return Math.Abs(a.Real - b.Real) < 1e-10 && 
               Math.Abs(a.Imaginary - b.Imaginary) < 1e-10;
    }
}
