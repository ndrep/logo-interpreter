from liblet import Stack, AnnotatedTreeWalker
from operator import add, mul, sub
from turtle import *
from functools import reduce
from random import randrange, seed
from math import radians, degrees, sin, log, log10, cos, atan, e, sqrt, exp, pow, pi
from parser import parse
import sys

sys.tracebacklimit = 0


interpreter = AnnotatedTreeWalker("type")


def __and(ast, visit, n):
    count = 0
    while count < n:
        b = visit(ast.children[count])
        if not isinstance(b, bool):
            raise TypeError("Logical operators only support boolean types")
        count += 1
        if not b:
            return False
    return True


def __or(ast, visit, n):
    count = 0
    while count < n:
        b = visit(ast.children[count])
        if not isinstance(b, bool):
            raise TypeError("Logical operators only support boolean types")
        count += 1
        if b:
            return True
    return False


def __not(ast, visit, n):
    b = visit(ast.children[0])
    if not isinstance(b, bool):
        raise TypeError("Logical operators only support boolean types")
    return not b


def make(a, b):

    interpreter.GLOBAL_MEMORY[a] = b


def _retval(a):
    if len(interpreter.ACTIVATION_RECORDS) == 1:
        raise SyntaxError("The OUTPUT command can only be executed in procedures")
    interpreter.ACTIVATION_RECORDS.peek()["OUTPUT"] = a[0]


def _retnone():
    if len(interpreter.ACTIVATION_RECORDS) == 1:
        raise SyntaxError("the STOP command can only be executed in procedures")
    interpreter.ACTIVATION_RECORDS.peek()["OUTPUT"] = None


def div(number):
    if len(number) == 1:
        if number[0] != 0:
            return 1 / number[0]
        else:
            raise ZeroDivisionError("Impossible to divide by 0")
    else:
        if number[1] != 0:
            result = number[0] / number[1]
            if number[0] % number[1] == 0:
                return int(result)
            else:
                return result
        else:
            raise ZeroDivisionError("Impossible to divide by 0")


def print_(a):
    for s in a:
        print(s)


def radarctan(number):
    if len(number) == 1:
        return atan(number[0])
    elif number[0] == 0 and number[1] > 0:
        return pi / 2
    elif number[0] == 0 and number[1] < 0:
        return -pi / 2
    else:
        return atan(number[1] / number[0])


def remainder(number):
    if not all(isinstance(x, int) for x in number):
        raise TypeError("Parameters must be integers")
    new_num = number
    result = abs(new_num[0]) % abs(new_num[1])
    if number[0] < 0 < result:
        return -result
    elif number[0] < 0 and result < 0:
        return result
    elif number[0] > 0 > result:
        return -result
    else:
        return result


def setpencolor(number):
    pencolor([n / 100 for n in number])


def rerandom(number):
    if len(number) == 0:
        seed(0)
    else:
        seed(number[0])


DISPATCH_TABLE = {
    "=": lambda x: x[0] == x[1],
    "<>": lambda x: not (x[0] == x[1]),
    "+": lambda x: x[0] + x[1],
    "sum_": lambda x: reduce(add, x),
    "*": lambda x: x[0] * x[1],
    "product": lambda x: reduce(mul, x),
    "-": lambda x: x[0] - x[1],
    "difference": lambda x: reduce(sub, x),
    "/": lambda x: div(x),
    "quotient": lambda x: div(x),
    "round_": lambda x: reduce(round, x),
    "sqrt_": lambda x: reduce(sqrt, x),
    "exp": lambda x: reduce(exp, x),
    "log10": lambda x: reduce(log10, x),
    "ln": lambda x: log(x[0], e),
    "cos": lambda x: cos(radians(x[0])),
    "radcos": lambda x: cos(x[0]),
    "sin": lambda x: sin(radians(x[0])),
    "radsin": lambda x: sin(x[0]),
    "arctan": lambda x: degrees(atan(x[0])),
    "radarctan": lambda x: radarctan(x),
    "lessp": lambda x: x[0] < x[1],
    "<": lambda x: x[0] < x[1],
    "greaterp": lambda x: x[0] > x[1],
    ">": lambda x: x[0] > x[1],
    "lessequalp": lambda x: x[0] <= x[1],
    "<=": lambda x: x[0] <= x[1],
    "greaterequalp": lambda x: x[0] >= x[1],
    ">=": lambda x: x[0] >= x[1],
    "minus": lambda x: -1 * x[0],
    "int_": lambda x: int(x[0]),
    "modulo": lambda x: x[0] % x[1],
    "power": lambda x: pow(x[0], x[1]),
    "remainder": lambda x: remainder(x),
    "and_": __and,
    "or_": __or,
    "not_": __not,
    "make": lambda x: make(x[0], x[1]),
    "fd": lambda x: forward(x[0]),
    "rt": lambda x: right(x[0]),
    "bk": lambda x: back(x[0]),
    "lt": lambda x: left(x[0]),
    "seth": lambda x: setheading(x[0]),
    "setpensize": lambda x: pensize(x[0]),
    "setpencolor": lambda x: setpencolor(x[0]),
    "output": _retval,
    "stop": _retnone,
    "rw": input,
    "setx": lambda x: setx(x[0]),
    "sety": lambda x: sety(x[0]),
    "setxy": lambda x: setpos(x[0], x[1]),
    "home": home,
    "random": lambda x: randrange(0, x[0]),
    "rerandom": lambda x: rerandom(x),
    "pu": penup,
    "pd": pendown,
    "cs": clearscreen,
    "st": showturtle,
    "ht": hideturtle,
    "clean": clearstamps,
    "arc": lambda x: circle(x[0], x[1]),
    "pr": print_,
}


@interpreter.register
def prog(visit, ast):
    for child in ast.children:
        visit(child)


@interpreter.register
def line(visit, ast):
    for child in ast.children:
        visit(child)


@interpreter.register
def block(visit, ast):
    lista = [visit(child) for child in ast.children]
    for child in lista[::-1]:
        if child is not None:
            return child


@interpreter.register
def rgbList(visit, ast):
    lista = [visit(child) for child in ast.children]
    for n in lista:
        if n > 100 or n < 0:
            raise ValueError("Parameter insertion error")
    return lista


@interpreter.register
def parameter(visit, ast):
    for child in ast.children:
        return visit(child)


@interpreter.register
def muldivOperator(visit, ast):
    return ast.root["name"]


@interpreter.register
def addsubOperator(visit, ast):
    return ast.root["name"]


@interpreter.register
def compareOperator(visit, ast):
    return ast.root["value"]


@interpreter.register
def string(visit, ast):
    return ast.root["name"]


@interpreter.register
def valueNumber(visit, ast):
    if "." in ast.root["value"]:
        return float(ast.root["value"])
    else:
        return int(ast.root["value"])


@interpreter.register
def deref(visit, ast):
    if len(ast.children) == 1:
        return interpreter.GLOBAL_MEMORY[visit(ast.children[0])]
    elif (
        len(interpreter.ACTIVATION_RECORDS) != 0
        and ast.root["name"] in interpreter.ACTIVATION_RECORDS.peek()
    ):
        return interpreter.ACTIVATION_RECORDS.peek()[ast.root["name"]]
    else:
        if ast.root["name"] not in interpreter.GLOBAL_MEMORY:
            raise NameError("Variable not found in global memory")
        return interpreter.GLOBAL_MEMORY[ast.root["name"]]


@interpreter.register
def boolean(visit, ast):
    if ast.root["value"][0] == '"':
        if ast.root["value"][1:].upper() == "FALSE":
            return False
        else:
            return True
    else:
        if ast.root["value"].upper() == "FALSE":
            return False
        else:
            return True


@interpreter.register
def expression(visit, ast):
    if len(ast.children) == 1:
        if "sign" in ast.root and ast.root["sign"] == "-":
            return -1 * visit(ast.children[0])
        elif "sign" in ast.root and ast.root["sign"] == "+":
            return 1 * visit(ast.children[0])
        else:
            return visit(ast.children[0])
    else:
        lista = [
            visit(child) for child in ast.children if child.root["type"] == "expression"
        ]
        op = visit(ast.children[1])
        if isinstance(lista[0], (bool, str)):
            raise TypeError("<" + str(lista[0]) + ">" + " it is not a valid value")
        if isinstance(lista[1], (bool, str)):
            raise TypeError("<" + str(lista[1]) + ">" + " it is not a valid value")
        return DISPATCH_TABLE[op](lista)


@interpreter.register
def ifStat(visit, ast):
    cond, stat = ast.children
    if not isinstance(visit(cond), bool):
        raise TypeError("Only True or False values are allowed")
    if visit(cond):
        visit(stat)


@interpreter.register
def ifElseStat(visit, ast):
    cond, true, false = ast.children
    if not isinstance(visit(cond), bool):
        raise TypeError("Only True or False values are allowed")
    if visit(cond):
        return visit(true)
    else:
        return visit(false)


@interpreter.register
def repeatStat(visit, ast):
    count, block = ast.children
    count = visit(count)
    if not isinstance(count, int):
        raise TypeError("<" + str(count) + ">" + " it is not a valid value")
    for _ in range(int(count)):
        if len(interpreter.ACTIVATION_RECORDS) != 0:
            local_memory = interpreter.ACTIVATION_RECORDS.peek()
            if "OUTPUT" in local_memory:
                return
        visit(block)


@interpreter.register
def whileStat(visit, ast):
    cond = visit(ast.children[0])
    if not isinstance(cond, bool):
        raise TypeError("<" + str(cond) + ">" + " it is not a valid value")
    while cond:
        if len(interpreter.ACTIVATION_RECORDS) != 0:
            local_memory = interpreter.ACTIVATION_RECORDS.peek()
            if "OUTPUT" in local_memory:
                return
        visit(ast.children[1])
        cond = visit(ast.children[0])


@interpreter.register
def command(visit, ast):
    local_memory = interpreter.ACTIVATION_RECORDS.peek()
    if "OUTPUT" in local_memory:
        return
    command = ast.root["name"]
    if command == "and_" or command == "or_" or command == "not_":
        return DISPATCH_TABLE[command](ast, visit, len(ast.children))
    elif len(ast.children) == 0 and command != "rerandom":
        return DISPATCH_TABLE[command]()
    else:
        lista = [visit(child) for child in ast.children]
        if (
            any(isinstance(x, bool) for x in lista)
            and command != "make"
            and command != "pr"
        ):
            raise TypeError("The parameters must be int or float")
        else:
            return DISPATCH_TABLE[command](lista)


@interpreter.register
def procedureInvocation(visit, ast):
    if ast.root["name"] not in interpreter.FUNCTIONS:
        raise NameError("Non-existent procedure")
    function = interpreter.FUNCTIONS[ast.root["name"]]
    arg = [visit(arg) for arg in ast.children]
    if len(function.root["params"]) != len(arg):
        raise TypeError("The number of parameters is wrong")
    interpreter.ACTIVATION_RECORDS.push(dict(zip(function.root["params"], arg)))
    local_memory = interpreter.ACTIVATION_RECORDS.peek()
    for child in function.children:
        if "OUTPUT" in local_memory:
            break
        visit(child)
    if "OUTPUT" in local_memory:
        return interpreter.ACTIVATION_RECORDS.pop()["OUTPUT"]
    else:
        interpreter.ACTIVATION_RECORDS.pop()


@interpreter.register
def procedureDeclaration(visit, ast):
    interpreter.FUNCTIONS[ast.root["name"]] = ast


def run(source):
    interpreter.GLOBAL_MEMORY = {}
    interpreter.FUNCTIONS = {}
    interpreter.ACTIVATION_RECORDS = Stack([{}])
    return interpreter(parse(source))
