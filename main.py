class Coder:
    def __init__(self, polynomial='1101', d=3, k=4, n=7,
                 vector_e=None):  # input from the highest degree of the polynomial in left
        if vector_e is None:
            vector_e = [0, 0, 0, 0, 0, 0, 0]
        # vector_e = vector_e[::-1]
        self.polynomial = []
        for symbol in polynomial:
            if symbol == '1':
                self.polynomial.append(1)
            elif symbol == '0':
                self.polynomial.append(0)
            else:
                raise Exception('Неправильный ввод полинома')
        self.polynomial = self.polynomial[::-1]  # highest degree of the polynomial in right
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
        m = []
        for i in message:
            if i == '1':
                m.append(1)
            elif i == '0':
                m.append(0)
            else:
                raise Exception('Неправильный ввод последовательности')
        m = m[::-1]
        r = len(self.polynomial) - 1
        _, c = poly_div_mod(m + [0] * r, self.polynomial)
        a = poly_sum(m + [0] * r, c)

        return a

    def add_errors(self, a: list) -> list:
        for i in range(len(self.vector_e)):
            if self.vector_e[i] == 1:
                a[i] = (a[i] + 1) % 2
        return a

    def decode(self, b: list) -> bool:
        _, s = poly_div_mod(b, self.polynomial)
        for i in s:
            if i != 0:
                return True
        return False


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
        if (_a[0] + _b[0]) == 1:
            temp_deg -= 1
            quotient.append(0)
            _a = _a[1:]
            continue

        for i, ab in enumerate(zip(_a, _b)):
            a_i = ab[0]
            b_i = ab[1]
            _a[i] = (a_i + b_i) % 2

        quotient.append(1)
        temp_deg -= 1
        _a = _a[1:]
        a = _a.copy()

    # delete the leading zeros
    while len(a) > 1 and a[0] == 0:
        a = a[1:]
    while len(quotient) > 1 and quotient[0] == 0:
        quotient = quotient[1:]
    quotient = quotient[::-1]
    a = a[::-1]
    return quotient, a


def poly_sum(a: list, b: list) -> list:
    a = a.copy()
    b = b.copy()
    if len(a) < len(b):
        a, b = b, a
    for i in range(len(b)):
        a[i] += b[i]
    return [x % 2 for x in a]


def main():
    coder = Coder()
    print(coder)
    l = '1111'
    print("a = " + str(a := coder.code(l)))
    print("b = " + str(b := coder.add_errors(a)))
    print(f'E = : {coder.decode(b)}')


if __name__ == '__main__':
    # print(poly_div_mod([0, 1, 1, 0], [1, 1]))
    print(poly_div_mod([1, 0, 1], [1, 1]))
    main()
