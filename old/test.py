# a = 1.8
# print(a)
# print(a,type(a))
# print(10 // 3)
# print(round(10 / 3,2))
# print(10 % 3)

a = lambda x, y: x + y
print(a(3, 4))


def func(x, y):
    return x + y


print(func(5, 6))


def test(f, a, b):
    print("test")
    print(f(a, b))


test(func, 3, 5)

re = map((lambda x,y: x+y),[1,2,3],[6,7,9])
print(re)
