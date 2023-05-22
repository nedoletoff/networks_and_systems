import itertools
import math
import random
import matplotlib.pyplot as plt
import threading
import time


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
        res += ' = ' + str(self.polynomial)
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
        # highest degree of the message in right
        m = []
        for i in message:
            if i == '1':
                m.append(1)
            elif i == '0':
                m.append(0)
            else:
                raise Exception('Неправильный ввод последовательности')
        r = len(self.polynomial) - 1
        mes = [0] * r + m
        _, c = poly_div_mod(mes, self.polynomial)
        a = poly_sum(c, mes)
        return a

    def add_errors(self, a: list) -> list:
        for i in range(len(self.vector_e)):
            if self.vector_e[i] == 1:
                a[i] = (a[i] + 1) % 2
        return a

    def decode(self, b: list) -> bool:
        _, s = poly_div_mod(b, self.polynomial)
        # print(f'{s=}')
        for i in s:
            if i != 0:
                return True
        return False


def poly_prod(a_p: list, b_p: list) -> list:  # highest degree of the polynomial in right
    a_p = a_p.copy()
    b_p = b_p.copy()
    # highest degree of the polynomial in left
    a_p = a_p[::-1]
    b_p = b_p[::-1]
    res = [0] * (len(a_p) + len(b_p) - 1)
    for i in range(len(a_p)):
        for j in range(len(b_p)):
            res[i + j] += (a_p[i] * b_p[j])
    res = res[::-1]
    # highest degree of the polynomial in right
    return [x % 2 for x in res]


def poly_div_mod(a_p: list, b_p: list) -> (list, list):  # highest degree of the polynomial in right
    a_p = a_p.copy()
    b_p = b_p.copy()
    a_p = a_p[::-1]
    b_p = b_p[::-1]
    # highest degree of the polynomial in left
    while a_p[0] == 0 and len(a_p) > 1:
        a_p = a_p[1:]
    while b_p[0] == 0 and len(b_p) > 1:
        b_p = b_p[1:]
    # delete the leading zeros
    a_deg = len(a_p) - 1
    b_deg = len(b_p) - 1
    temp_deg = a_deg - b_deg
    quotient = []
    _a = a_p.copy()
    while temp_deg >= 0:
        _b = b_p.copy() + [0] * temp_deg
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
        a_p = _a.copy()

    # delete the leading zeros
    while len(a_p) > 1 and a_p[0] == 0:
        a_p = a_p[1:]
    while len(quotient) > 1 and quotient[0] == 0:
        quotient = quotient[1:]
    # highest degree of the polynomial in right
    quotient = quotient[::-1]
    a_p = a_p[::-1]
    return quotient, a_p


def poly_sum(a_p: list, b_p: list) -> list:
    a_p = a_p.copy()
    b_p = b_p.copy()
    if len(a_p) < len(b_p):
        a_p, b_p = b_p, a_p
    for i in range(len(b_p)):
        a_p[i] += b_p[i]
    res = [x % 2 for x in a_p]
    return res


def main():
    coder = Coder()
    print(coder)
    l = '1001'
    print("a = " + str(a := coder.code(l)))
    print("b  = " + str(b := coder.add_errors(a)))
    print(f'E = : {coder.decode(b)}\n')

    coder.vector_e = [1, 0, 1, 0, 0, 0, 1]
    print(coder)
    print("a = " + str(a := coder.code(l)))
    print("b  = " + str(b := coder.add_errors(a)))
    print(f'E = : {coder.decode(b)}')


def get_pr_error_not_find():
    coder = Coder()
    print(coder)
    errors = 0
    all_var = 0
    temp_vector_e = list(range(7))
    all_combinations = []
    '''
    all_combinations = list(itertools.combinations(temp_vector_e, 1)) + list(itertools.combinations(temp_vector_e, 2)) + \
                    list(itertools.combinations(temp_vector_e, 3))
    '''
    for i in range(4, 7 + 1):
        all_combinations += list(itertools.combinations(temp_vector_e, i))
    all_vectors_e = []
    for i in all_combinations:
        temp_vector_e = [0] * 7
        for j in i:
            temp_vector_e[j] = 1
        all_vectors_e.append(temp_vector_e.copy())

    l = '1001'
    print("a = " + str(a := coder.code(l)))
    for i in all_vectors_e:
        coder.vector_e = i
        # print("b  = " + str(b := coder_.add_errors(a)))
        # print(f'E = : {coder_.decode(b)}')
        b = coder.add_errors(a)
        if coder.decode(b):
            errors += 1
        else:
            print(f'vector_e: {i}')
        all_var += 1
    print(f'pr(нашел ошибку) = {errors}/{all_var} = {errors / all_var}')


def get_pr_error_in_decode(epsilon, p_error, len_l, coder_, res=None):
    if res is None:
        res = [0]
    N_examples = 9 / (4 * math.pow(epsilon, 2))
    N_examples = int(N_examples)
    errors_n = 0
    for i in range(N_examples):
        l = ''
        for j in range(len_l):
            l += str(random.randint(0, 1))
        a = coder_.code(l)

        vector_e = [0] * 7
        for j in range(len_l):
            if random.random() < p_error:
                vector_e[j] = 1
        coder_.vector_e = vector_e

        b = coder_.add_errors(a)
        if not (coder_.decode(b)) and vector_e.__contains__(1):
            errors_n += 1
    res[0] = errors_n / N_examples
    return errors_n, N_examples


def test_poly():
    a = [0, 0, 0, 1, 1, 1, 1]
    l = [1, 0, 1, 1]
    print(poly_div_mod(a, l))
    print(poly_div_mod([0, 1, 1, 0], [1, 1]))
    print(p := poly_prod([1, 1, 1, 1], [1, 1]))
    print(p := poly_sum(p, [1, 1, 1, 1, 1]))
    print(poly_div_mod(p, [1, 1]))


def no_threading():
    probabilities = []
    coder = Coder()
    print(coder)
    for i in range(10):
        probabilities.append(i / 10)

    for j in range(2, 7 + 1):
        #print('len l = ' + str(j))
        res = []
        for p in probabilities:
            #print('p = ' + str(p))
            errors_n, N_examples = get_pr_error_in_decode(0.01, p, j, coder)
            #print(f'{errors_n=}, {N_examples=}, {errors_n / N_examples=:.2f}')
            res.append(errors_n / N_examples)
        plt.plot(probabilities, res, label=f'len l= {j}')
    plt.legend()
    plt.xlabel('p ошибки при передаче')
    plt.ylabel('pr(не нашел ошибку)')
    plt.title('График ошибок декодирования k = 4')
    plt.grid()
    plt.savefig('graph.png')
    #plt.show()


def use_threading():
    probabilities = []
    coder = Coder()
    print(coder)
    for i in range(10):
        probabilities.append(i / 10)

    for k in range(2, 7 + 1):
        #print('len l = ' + str(k))
        result = [[0] * 10 for i in range(10)]
        t = [threading.Thread(target=get_pr_error_in_decode, args=(0.01, p, k, Coder(), result[int(p*10)])) for p in probabilities]
        for i in t:
            i.start()
        for i in t:
            i.join()
        result = [i[0] for i in result]
        plt.plot(probabilities, result, label=f'len l= {k}')
    plt.legend()
    plt.xlabel('p ошибки при передаче')
    plt.ylabel('pr(не нашел ошибку)')
    plt.title('График ошибок декодирования k = 4')
    plt.grid()
    plt.savefig('graph.png')
    #plt.show()


if __name__ == '__main__':
    start_time = time.time()
    no_threading()
    print(f'Время выполнения no threading: {time.time() - start_time}')
    start_time = time.time()
    use_threading()
    print(f'Время выполнения use threading: {time.time() - start_time}')
