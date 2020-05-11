def iter_improve(update , test, guess = 1):
    while not test(guess):
        guess = update(guess)
    return guess

def square(x):
    return x*x

def near(x, f, g):
    return approx_eq(f(x), g(x))

def approx_eq(x, y, tolerance = 1e-5):
    return abs(x - y)< tolerance

def golden_update(guess):
    return 1/guess +1

# def golden_test():
#     return near(guess, square, successor)

# def square_root(x):
#     def update(guess):
#         return average(guess, x/guess)
#     def test(guess):
#         return approx_eq(square(guess), x)
#     return iter_improve(update, test)

def compose1(f, g):
    def h(x):
        return f(g(x))
    return h

def square_root(a):
    return find_root(lambda x: square(x) - a)

def logarithm(a, base = 2):
    return find_root(lambda x: pow(base, x) - a)

def approx_derivative(f, x, delta = 1e-5):
    df = f(x + delta) - f(x)
    return df/delta

def newton_update(f):
    def update(x):
        return x -f(x) / approx_derivative(f, x)
    return update

def find_root(f, initial_guess = 10):
    def test(x):
        return approx_eq(f(x), 0)
    return iter_improve(newton_update(f), test, initial_guess)

# print(square_root(16))
# print(logarithm(32, 2))

empty_rlist = None
def make_rlist(first, rest):
    return (first, rest)

def first(s):
    return s[0]

def rest(s):
    return s[1]

def len_rlist(s):
    length = 0
    while s != empty_rlist:
        s, length = rest(s), length + 1
    return length

def getitem_rlist(s, i):
    while i > 0:
        s, i = rest(s), i-1
    return first(s)

# counts = make_rlist(1, make_rlist(2, make_rlist(3, make_rlist(4, empty_rlist))))

# print(len_rlist(counts))
# print(getitem_rlist(counts, 1))

def make_withdraw(balance):
    def withdraw(amount):
        nonlocal balance
        if amount >balance:
            return 'Insufficient funds'
        balance = balance - amount
        return balance
    return withdraw

def make_mutable_rlist():
    contents = empty_rlist
    def dispatch(message, value = None):
        nonlocal contents
        if message == 'len':
            return len_rlist(contents)
        elif message == 'getitem':
            return getitem_rlist(contents, value)
        elif message == 'push_first':
            contents = make_rlist(value, contents)
        elif message == 'pop_first':
            f = first(contents)
            contents = rest(contents)
            return f
        elif message == 'str':
            return str(contents)
    return dispatch

def to_muable_rlist(source):
    s = make_mutable_rlist()
    for element in reversed(source):
        s('push_first', element)
    return s
# suits = ['coin', 'string', 'myriad'] 
# s = to_muable_rlist(suits)
# print(type(s))
# print(s('str'))

def make_dict():
    records = []
    def getitem(key):
        for k, v in records:
            if k == key:
                return v
    def setitem(key, value):
        for item in records:
            if item[0] == key:
                item[1] = value
                return
        records.append([key, value])
    def dispatch(message, key = None, value = None):
        if message == 'getitem':
            return getitem(key)
        elif message == 'setitem':
            setitem(key, value)
        elif message == 'keys':
            return tuple(k for k, _ in records)
        elif message == 'values':
            return tuple(v for _, v in records)
    return dispatch



from operator import add, sub , mul, truediv

def adder(a, b, c):
    return make_ternary_constraint(a, b, c, add, sub, sub)

def multiplier(a, b, c):
    return make_ternary_constraint(a, b, c, mul, truediv, truediv)

def constant(connector, value):
    constraint = {}
    connector['set_val'](constraint, value)
    return constraint

def make_ternary_constraint(a, b, c, ab, ca, cb):
    def new_value():
        av, bv, cv = [connector['has_val']() for connector in (a, b, c)]
        if av and bv:
            c['set_val'](constraint, ab(a['val'], b['val']))
        elif av and cv:
            b['set_val'](constraint, ca(c['val', a['val']]))
        elif bv and cv:
            a['set_val'](constraint, cb(c['val'], b['val']))
    def forget_value():
        for connector in (a, b, c):
            print(connector)
            connector['forget'](constraint)
    constraint = {'new_val': new_value, 'forget': forget_value}
    for connector in (a, b, c):
        connector['connect'](constraint)

def make_converter(c, f):
    u ,v , w, x, y =[make_connector() for _ in range(5)]
    multiplier(c, w, u)
    multiplier(v, x, u)
    adder(v, y, f)
    constant(w, 9)
    constant(x, 5)
    constant(y, 32)

def make_connector(name=None):
    informant = None
    constraints = []
    def set_value(source, value):
        nonlocal informant
        val = connector['val']
        if val is None:
            informant, connector['val'] = source, value
            if name is not None:
                print(name, '=', value)
            inform_all_except(source, 'new_val', constraints)
        else:
            if val != value:
                print('Contradiction detected:', val, 'vs', value)
    def forget_value(source):
        nonlocal informant
        if informant == source:
            informant, connector['val'] = None, None
            if name is not None:
                print(name, 'is forgotten')
            inform_all_except(source, 'forget', constraints)
    connector = {'val': None,
                'set_val': set_value,
                'forget': forget_value,
                'has_val': lambda: connector['val'] is not None,
                'connect': lambda source: constraints.append(source)
                }
    return connector

def inform_all_except(source, message, constraints):
    for c in constraints:
        if c != source:
            c[message]()

celsius = make_connector('Celsius')
fahrenheit = make_connector('Fahrenheit')
make_converter(celsius, fahrenheit)
celsius['set_val']('user', 25)
celsius['forget']('user')