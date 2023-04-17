class Coder:
    def __init__(self, polynomial='1101', d=3, k=4, n=7,
                 vector_e=None):  # input from the highest degree of the polynomial in left
        if vector_e is None:
            vector_e = [0, 0, 0, 0, 0, 0, 0]
        vector_e = vector_e[::-1]
        self.polynomial = []
        for symbol in polynomial:
            if symbol == '1':
                self.polynomial.append(1)
            elif symbol == '0':
                self.polynomial.append(0)
            else:
                raise Exception('Неправильный ввод полинома')
        self.polynomial = self.polynomial[::-1] # highest degree of the polynomial in right
        self.k = k
        self.n = n
        self.d = d
        self.vector_e = vector_e

    def __str__(self):
        res = ''
        for i, symbol in enumerate(self.polynomial):
            if symbol == 1:
                res += 'x^' + str(i)
                res += '+'
        res = res[:-1]
        res += '\n'
        res += 'k = ' + str(self.k) + '\n'
        res += 'n = ' + str(self.n) + '\n'
        res += 'd = ' + str(self.d) + '\n'
        res += 'Вектор ошибки: ' + str(self.vector_e) + '\n'
        return res

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.polynomial == other.polynomial and self.k == other.k and self.n == other.n and \
               self.vector_e == other.vector_e and self.d == other.d

    def code(self, message: str) -> list:
        l = []
        for i in message:
            if i == '1':
                l.append(1)
            elif i == '0':
                l.append(0)
            else:
                raise Exception('Неправильный ввод последовательности')
        l = l[::-1]
        res = []

        return res


def poly_prod(a: list, b: list) -> list:
    a = a[::-1]
    b = b[::-1]
    res = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            res[i + j] += (a[i] * b[j])
    res = res[::-1]
    return [x % 2 for x in res]


def poly_div_mod(a: list, b: list) -> (list, list):  # highest degree of the polynomial in right
    a = a.copy()
    b = b.copy()
    a = a[::-1]
    b = b[::-1]
    # highest degree of the polynomial in left
    while a[0] == 0:
        a = a[1:]
    while b[0] == 0:
        b = b[1:]
    # delete the leading zeros
    a_deg = len(a) - 1
    b_deg = len(b) - 1
    temp_deg = a_deg - b_deg
    quotient = []
    _a = a.copy()
    while temp_deg >= 0:
        _b = b.copy() + [0] * temp_deg
        if (_a[-1] + _b[-1]) == 1:
            temp_deg -= 1
            quotient.append(0)
            continue

        for i, ab in enumerate(zip(_a, _b)):
            a_i = ab[0]
            b_i = ab[1]
            _a[i] = (a_i + b_i) % 2

        quotient.append(1)
        temp_deg -= 1
        a = _a.copy()

    quotient.append(0)
    quotient = quotient[::-1]

    # delete the leading zeros
    while len(a) > 1 and a[0] == 0:
        a = a[1:]
    while len(quotient) > 1 and quotient[0] == 0:
        quotient = quotient[1:]
    return quotient, a


def coder_input() -> Coder:
    # polynomial = input('Введите полином: ')
    # k = int(input('Введите коэффициент: '))
    """
    vector = input('Введите вектор ошибки: ')
    vector_e = []
    for i in vector:
        if i == '1':
            vector_e.append(1)
        elif i == '0':
            vector_e.append(0)
        else:
            raise Exception('Неправильный ввод вектора ошибки')
    vector_l = input('Введите последовательность: ')

    """
    return Coder()


def main():
    coder = coder_input()
    print(coder)


if __name__ == '__main__':
    print(poly_prod([1, 1], [1, 1]))
    print(poly_div_mod([1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0]))
    print(poly_div_mod([1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]))
    print(poly_div_mod([1, 0, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1]))
    print(poly_div_mod([1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0]))
    main()
