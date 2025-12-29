import sys

aflag = 0
bflag = 0
cflag = 0
l = len(sys.argv)
for i in range(1, l):
    if complex(sys.argv[i]).imag == 0:
        if aflag == 0:
            a = complex(sys.argv[i])
            aflag = 1
        else:
            if bflag == 0:
                b = complex(sys.argv[i])
                bflag = 1
            else:
                c = complex(sys.argv[i])
                cflag = 1
                break

if aflag == 0:
    x = complex(input())
    while x.imag != 0:
        x = complex(input())
    a = x
if bflag == 0:
    x = complex(input())
    while x.imag != 0:
        x = complex(input())
    b = x
if cflag == 0:
    x = complex(input())
    while x.imag != 0:
        x = complex(input())
    c = x

#if len(sys.argv) > 1:
#    a = complex(sys.argv[1])
#else:
#    a = complex(input())
#if len(sys.argv) > 2:
#    b = complex(sys.argv[2])
#else:
#    b = complex(input())
#if len(sys.argv) > 3:
#    c = complex(sys.argv[3])
#else:
#    c = complex(input())
x1 = ((-b+(b**2-4*a*c)**0.5)/(2*a))**0.5
x2 = ((-b-(b**2-4*a*c)**0.5)/(2*a))**0.5
x3 = -((-b+(b**2-4*a*c)**0.5)/(2*a))**0.5
x4 = -((-b-(b**2-4*a*c)**0.5)/(2*a))**0.5
d = b**2-4*a*c
print('D =', d.real if d.imag == 0 else d)
print('Действительные корни:')
if x1.imag == 0:
    print(x1.real)
if x2.imag == 0 and x1 != x2:
    print(x2.real)
if x3.imag == 0 and x1 != x3 and x2 != x3:
    print(x3.real)
if x4.imag == 0 and x1 != x4 and x2 != x4 and x3 != x4:
    print(x4.real)
input("Нажмите Enter для выхода")
