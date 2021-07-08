from os import path, getcwd, listdir
file = path.join(getcwd(), listdir(getcwd())[0])
here = path.dirname(path.dirname(file))
print(here)
from src.logo.interpreter import run
from src.logo.parser import parse

COMMAND_TESTS = {
    "op_precedence": [
        r"""
            PR 2 * 3 + 4
        """,
        "10\n",
    ],
    "list_expression": [
        r"""
            if [true false true make "a "name True] [pr 2]
        """,
        "2\n",
    ],
    "op_precedence_unary": [
        r"""
            PR -1 + 1
        """,
        "0\n",
    ],
    "simple_make": [
        r"""
            MAKE "A 123
            PR :A
        """,
        "123\n",
    ],
    "make_with_expr_name": [
        r"""
            MAKE "NAME "ALIAS
            MAKE :NAME 123
            PR :ALIAS
        """,
        "123\n",
    ],
    "simlpe_thing": [
        r"""
            MAKE "NAME 123
            PRINT THING "NAME
        """,
        "123\n",
    ],
    "thing_with_expr_name": [
        r"""
            MAKE "NAME "ALIAS
            MAKE "ALIAS 123
            PRINT THING :NAME

        """,
        "123\n",
    ],
    "if_as_statement_true": [
        r"""
            IF "TRUE [PRINT 1]
            PRINT 2
        """,
        "1\n2\n",
    ],
    "if_as_statement_false": [
        r"""
            IF FALSE [PRINT 1]
            PRINT 2
        """,
        "2\n",
    ],
    "ifelse_as_statement_true": [
        r"""
            IFELSE "TRue [PRINT 1] [PRINT 2]
            PRINT 3
        """,
        "1\n3\n",
    ],
    "ifelse_as_statement_false": [
        r"""
            IFELSE "FALSE [PRINT 1] [PRINT 2]
            PRINT 3
        """,
        "2\n3\n",
    ],
    "ifelse_as_operation_true": [
        r"""
            PRINT 1 + IFELSE "TRue [1] [2]
            PRINT 3
        """,
        "2\n3\n",
    ],
    "ifelse_as_operation_multiple_expr": [
        r"""
            PRINT 1 + IFELSE "TRue [1 2 3] [4]
            PRINT 5
        """,
        "4\n5\n",
    ],
    "ifelse_as_operation_side_effects": [
        r"""
            PRINT 1 + IFELSE "TRue [MAKE "A 1 2 :A MAKE "A 3] [3]
            PRINT 4
        """,
        "2\n4\n",
    ],
    "ifelse_as_operation_false": [
        r"""
            PRINT 1 + IFELSE FALSE [1] [2]
            PRINT 3
        """,
        "3\n3\n",
    ],
    "short_circuit": [
        r"""
            MAKE "X 0
            IFELSE AND [NOT (:X = 0)] [(1 / :X) > .5] [PR 1] [PR 2]
            IFELSE (AND TRUE [NOT (:X = 0)] TRUE [(1 / :X) > .5] TRUE) [PR 1] [PR 3]
            MAKE "X 1
            IFELSE AND [NOT (:X = 0)] [(1 / :X) > .5] [PR 1] [PR 2]
        """,
        "2\n3\n1\n",
    ],
    "bool_expr_and_false": [
        r"""
            IF AND "TRUE "FALSE [PR 1] PR 2
            IF AND TRUE "FALSE [PR 3] PR 4
            IF AND "TRUE FALSE [PR 5] PR 6
            IF AND TRUE FALSE [PR 7] PR 8
        """,
        "2\n4\n6\n8\n",
    ],
    "bool_expr_and_true": [
        r"""
            IF AND "TRUE "TRUE [PR 1] PR 2
            IF AND TRUE "TRUE [PR 3] PR 4
            IF AND "TRUE TRUE [PR 5] PR 6
            IF AND TRUE TRUE [PR 7] PR 8
        """,
        "1\n2\n3\n4\n5\n6\n7\n8\n",
    ],
    "bool_expr_or_true": [
        r"""
            IF OR "TRUE "FALSE [PR 1] PR 2
            IF OR TRUE "FALSE [PR 3] PR 4
            IF OR "TRUE FALSE [PR 5] PR 6
            IF OR TRUE FALSE [PR 7] PR 8
        """,
        "1\n2\n3\n4\n5\n6\n7\n8\n",
    ],
    "bool_expr_or_false": [
        r"""
            IF OR "FALSE "FALSE [PR 1] PR 2
            IF OR FALSE "FALSE [PR 3] PR 4
            IF OR "FALSE FALSE [PR 5] PR 6
            IF OR FALSE FALSE [PR 7] PR 8
        """,
        "2\n4\n6\n8\n",
    ],
    "bool_three": [
        r"""
            IF AND [AND "TRUE TRUE] TRUE [PR 1] PR 2
        """,
        "1\n2\n",
    ],
    "repeat": [
        r"""
        MAKE "C 0
        REPEAT 4 [MAKE "C :C + 1]
        PR :C
        """,
        "4\n",
    ],
    "while": [
        r"""
        MAKE "C 0
        WHILE :C < 4 [MAKE "C :C + 1]
        PR :C
        """,
        "4\n",
    ],
    "func_biarg": [
        r"""
            TO FUNC :X :Y
                OUTPUT :X + :Y
            END

            PR (FUNC 3 4)
        """,
        "7\n",
    ],
    "stop": [
        r"""
            TO FUNC
                PR 1
                STOP
                PR 2
            END

            (FUNC)
        """,
        "1\n",
    ],
    "stop_repeat": [
        r"""
            TO FUNC
                REPEAT 4 [PR 1 STOP]
            END

            (FUNC)
        """,
        "1\n",
    ],
    "stop_while": [
        r"""
            TO FUNC
                MAKE "N 4
                WHILE :N > 0 [
                    MAKE "N :N - 1
                    PR 1
                    STOP
                ]
            END

            (FUNC)
        """,
        "1\n",
    ],
    "output_repeat": [
        r"""
            TO FUNC
                REPEAT 4 [PR 1 OUTPUT 2]
            END

            (FUNC)
        """,
        "1\n",
    ],
    "OUTPUT_while": [
        r"""
            TO FUNC
                MAKE "N 4
                WHILE :N > 0 [
                    MAKE "N :N - 1
                    PR 1
                    OUTPUT 2
                ]
            END

            (FUNC)
        """,
        "1\n",
    ],
    "output": [
        r"""
            TO FUNC
                PR 1
                OUTPUT 2
                PR 3
            END

            (FUNC)
        """,
        "1\n",
    ],
    "factorial": [
        r"""
            TO FACTORIAL :N
                IF :N = 0 [OUTPUT 1]
                OUTPUT :N * FACTORIAL :N - 1
            END
            PR (FACTORIAL 6)
        """,
        "720\n",
    ],
    "fibonacci": [
        r"""
            TO FIBONACCI :N
                IF :N <= 1 [OUTPUT :N]
                OUTPUT (FIBONACCI :N - 2) + (FIBONACCI :N - 1)
            END
            PR (FIBONACCI 7)
        """,
        "13\n",
    ],
    "ln_command": [
        r"""
            pr ln 10
        """,
        "2.302585092994046\n",
    ],
    "sin_command": [
        r"""
            pr sin 90
        """,
        "1.0\n",
    ],
    "pr_sign_number": [
        r"""
            pr --------3

        """,
        "3\n",
    ],
    "cos_command": [
        r"""
            pr cos 90
        """,
        "6.123233995736766e-17\n",
    ],
    "arctan_command": [
        r"""
            pr arctan 90
        """,
        "89.36340642403653\n",
    ],
    "lessp_command": [
        r"""
            pr lessp 30 90
            pr lessp 90 90
        """,
        "True\nFalse\n",
    ],
    "op_command": [
        r"""
            pr 300 < 90
            pr 300 > 90
            pr 90 <= 90
            pr 300 <= 90
            pr 300 >= 90
            pr 300 >= 300
            pr 300 = 300
            pr 0 = 1
        """,
        "False\nTrue\nTrue\nFalse\nTrue\nTrue\nTrue\nFalse\n",
    ],
    "greaterp_command": [
        r"""
            pr greaterp 30 90
            pr greaterp 90 90
        """,
        "False\nFalse\n",
    ],
    "<>_command": [
        r"""
            pr 0 <> 0
        """,
        "False\n",
    ],
    "lessequalp_command": [
        r"""
            pr lessequalp 30 90
            pr lessequalp 90 90
        """,
        "True\nTrue\n",
    ],
    "greaterequalp_command": [
        r"""
            pr greaterequalp 30 90
            pr greaterequalp 90 90
        """,
        "False\nTrue\n",
    ],
    "meno_unario": [r"""pr -(1+1+1+1-1-1-1-1-1)""", "1\n"],
    "espressioni": [r"""pr (1 + 1+1) * 2 / (1 / 1)""", "6\n"],
    "espressioni2": [r"""pr 2 * (3 + 1)""", "8\n"],
    "and_command": [
        r"""
            pr (and True FaLse FALSE "True True "FALSE)
        """,
        "False\n",
    ],
    "or_command": [
        r"""
            pr (or False FaLse FALSE "FALSE "TRUE)
        """,
        "True\n",
    ],
    "pr_command": [
        r"""
            pr "ciao
        """,
        "ciao\n",
    ],
    "pr_parenthesis_command": [
        r"""
            pr sum (((((((((5)))))))))(((((((((1)))))))))
        """,
        "6\n",
    ],
    "pr_multiple_command": [
        r"""
            (pr "ciao "mi "chiamo "Andrea)
        """,
        "ciao\nmi\nchiamo\nAndrea\n",
    ],
    "division_mult": [
        r"""
        pr 100/2/2*3/5
        """,
        "15\n",
    ],
    "pr_line_command": [r"""pr 30""", "30\n"],
    "parentesi_complessa_command": [
        r"""
        make "a "TrUe
        make "b True
        make "c "TRUE
        pr (((and ((:c)) (((((and :a :b))))))))
        """,
        "True\n",
    ],
    "stop_command": [
        r"""
        TO TESTSTOP
        REPEAT 2 [
            PR 1
            PR 3
            STOP
            PR 2
            ]
        END
        (TESTSTOP)
        PR 4
        """,
        "1\n3\n4\n",
    ],
    "test1": [
        r"""
        pr
        1
        +
        2
        """,
        "3\n",
    ],
    "test2": [
        r"""
        pr 2 + 4
        +
        1
        +
        2 * 4
        """,
        "15\n",
    ],
    "test3": [
        r"""
        (
        pr
        (
        sum
        3
        4
        5
        6
        )
        (
        sum
        3
        4
        5
        6
        )
        )
        """,
        "18\n18\n",
    ],
    "test4": [
        r"""
        (




        pr
        (
        product 3 4
        5
        )
        (product
        2
        3 6
        )
        )
        """,
        "60\n36\n",
    ],
    "test5": [
        r"""
        (
        pr

        quotient
        10
        5


        2
        *
        3
        /
        6

        )
        """,
        "2\n1\n",
    ],
    "test6": [
        r"""
        (pr sin 30 cos 30 arctan 30 radarctan 30 radsin 30 radcos 30)
        """,
        "0.49999999999999994\n0.8660254037844387\n88.09084756700362\n1.5374753309166493\n-0.9880316240928618\n0"
        ".15425144988758405\n",
    ],
}

PARSER_TESTS = {
    "parentesi": r"""
        pr and :c ((((and :a :b))))
    """,
    "commands": r"""

        ARC 1 2
        BACK 1
        BK 1
        CLEAN
        CLEARSCREEN
        CS
        FORWARD 1
        FD 1
        HIDETURTLE
        HT
        HOME
        LEFT 1
        LT 1
        MAKE "a 1
        PENDOWN
        PD
        PENUP
        PU
        PRINT 1
        PR 1
        ( PRINT 1 2 )
        RERANDOM
        ( RERANDOM 1 )
        RIGHT 1
        RT 1
        SETHEADING 1
        SETH 1
        SETPENCOLOR [ 1 2 3 ]
        SETPC [ 1 2 3 ]
        SETPENSIZE 1
        SETX 1
        SETXY 1 2
        SETY 1
        SHOWTURTLE
        ST
    """,
    "operations": r"""

        ( PRINT
            ARCTAN 1
            ( ARCTAN 1 1 )
            COS 1
            DIFFERENCE 1 2
            EXP 1
            GREATEREQUALP 1 2
            GREATEREQUAL? 1 2
            GREATERP 1 2
            GREATER? 1 2
            INT 1
            LESSEQUALP 1 2
            LESSEQUAL? 1 2
            LESSP 1 2
            LESS? 1 2
            LN 1
            LOG10 1
            MINUS 1
            MODULO 1 2
            POWER 1 2
            PRODUCT 1 2
            ( PRODUCT 1 2 3 )
            QUOTIENT 1 2
            ( QUOTIENT 1 )
            RADARCTAN 1
            ( RADARCTAN 1 1 )
            RADCOS 1
            RADSIN 1
            RANDOM 1
            ( RANDOM 1 1 )
            READWORD
            RW
            REMAINDER 1 2
            ROUND 1
            SIN 1
            SUM 1 2
            ( SUM 1 2 3 )
            SQRT 1
        )
    """,
    "dots": r"""

        PR :a
    """,
    "thing": r"""

        PR THING "a
    """,
    "make1": r"""
        MAKE "RESULT 1
    """,
    "make2": r"""
        MAKE :VAR AND [NOT (:X = 0)] [(1 / :X) > .5]

    """,
    "repeat": r"""

        repeat 4 [fd 100 rt 90]
    """,
    "while": r"""

        while :c < 1 [make "c :c + 1]

    """,
    "koch": r"""

        to line :count :length
         ifelse :count = 1 [fd :length] [
           make "count :count -1
           (line :count :length)
           lt 60 (line :count :length)
           rt 120 (line :count :length)
           lt 60 (line :count :length)
          ]
        end
        to koch :count :length
          rt 30 (line :count :length)
          rt 120 (line :count :length)
          rt 120 (line :count :length)
        end
        cs
        setxy  0 0
        (koch 5 5)

    """,
    "ifelse": r"""

        if :x < 1 [pr 2]
        ifelse "a = "b [pr 3] [pr 4]
        pr if :a = 0 [5]
        pr ifelse :a = 0 [6] [7]

    """,
    "userprocinv": r"""

        USER 1
        (USER 1 2 3)

    """,
    "logic1": r"""
        ( PRINT
            AND :a = 0 :b > 1
            ( AND :a = 0 :b > 1 NOT :c )
            OR  :a = 0 :b > 1
            ( OR :a = 0 :b > 1 NOT :c )
            NOT :c
        )
    """,
    "logic2": r"""

        ( PRINT
            AND [:a = 0 :b > 1] [:a = 0 :b > 1]
            ( AND [:a = 0 :b > 1] [:a = 0 :b > 1] [OR :c NOT :d] )
            OR  [:a = 0 :b > 1] [:a = 0 :b > 1]
            ( OR [:a = 0 :b > 1] [:a = 0 :b > 1] [OR :c NOT :d] )
            NOT [OR :c NOT :d]
        )
    """,
    "fern": r"""
        to fern :size :sign
          if :size < 1 [ stop ]
          fd :size
          rt 70 * :sign (fern :size * 0.5 :sign * -1) lt 70 * :sign
          fd :size
          lt 70 * :sign (fern :size * 0.5 :sign) rt 70 * :sign
          rt 7 * :sign (fern :size - 1 :sign) lt 7 * :sign
          bk :size * 2
        end
        clearscreen pu bk 150 pd
        (fern 25 1)
    """,
    "test_square": r"""

        to square :length
          repeat 4 [ fd :length rt 90 ]
        end
        to randomcolor
          setpencolor [random 100 random 100 random 100]
        end
        clearscreen
        repeat 36 [ (randomcolor) square random 200 rt 10 ]

    """,
    "test_tree": r"""

        TO tree :size
           if :size < 5 [forward :size back :size stop]
           forward :size/3
           left 30 tree :size*2/3 right 30
           forward :size/6
           right 25 tree :size/2 left 25
           forward :size/3
           right 25 tree :size/2 left 25
           forward :size/6
           back :size
        END
    clearscreen
    tree 150

    """,
}

TYPE_TESTS = {
    "while_fake": [
        r"""
        make "x "prova
        while :x < 10 [pr 3 + 5]
        """,
        TypeError,
    ],
    "command_fake2": [
        r"""
        pr sum 1 True
        """,
        TypeError,
    ],
    "pr_fake": [
        r"""
        print 1 + "commando
        """,
        TypeError,
    ],
    "if_fake": [
        r"""
        make "x "prova
        if :x < 10 [pr 3 + 5]
        """,
        TypeError,
    ],
    "quotient_fake": [
        r"""
        pr (quotient 0)
        """,
        ZeroDivisionError,
    ],
    "bool_fake": [
        r"""
        make "a 1
        pr and :a True
        """,
        TypeError,
    ],
    "ifelse_fake": [
        r"""
        make "x "prova
        ifelse :x = 10 [pr 3] [pr 4]
        """,
        TypeError,
    ],
    "repeat_fake": [
        r"""
        make "x "prova
        repeat :x [pr 3]
        """,
        TypeError,
    ],
    "procedure_fake": [
        r"""
        to n :x :y
        end
        (n 1 2 3)
        """,
        TypeError,
    ],
    "and_or_not_condition": [
        r"""
        and True 1
        """,
        TypeError,
    ],
    "command_fake": [
        r"""
        make "x "prova
        (sum 1 2 3 4 5 :x)
        """,
        TypeError,
    ],
    "repeat2_fake": [
        r"""
        repeat 3.3 [pr 4 + 5]
        """,
        TypeError,
    ],
    "procedure2_fake": [
        r"""
        (FUNC)
        """,
        NameError,
    ],
    "deref_fake": [
        r"""
        pr :a
        """,
        NameError,
    ],
    "expression_fake": [
        r"""
        make "x "prova
        pr 2 * 3 + :x
        """,
        TypeError,
    ],
    "multiplying_expression_fake": [
        r"""
        make "x "prova
        pr 2 * 3 * :x
        """,
        TypeError,
    ],
    "compare_fake": [
        r"""
        make "x "prova
        if and [:x < 10 2 = 2] TrUe [ not ( 3 > :x ) ] [pr "ciao]
        """,
        TypeError,
    ],
    "if2_fake": [
        r"""
        make "x "prova
        pr 23 + if  TrUe  [:x]
        """,
        TypeError,
    ],
    "ifelse2_fake": [
        r"""
        make "x "prova
        make :y "ciao
        pr 10 + ifelse and [True True True][True] [:y] [10]
        """,
        NameError,
    ],
    "deref2_fake": [
        r"""
        make "x "prova
        make :y "ciao
        pr 1 + :y
        """,
        NameError,
    ],
    "division_fake": [
        r"""
        pr 3 / 0
        """,
        ZeroDivisionError,
    ],
    "if_control": [
        r"""
        if 1 [pr 4]
        """,
        TypeError,
    ],
    "ifelse_control": [
        r"""
        ifelse 0 [pr 4][pr 5]
        """,
        TypeError,
    ],
    "while_control": [
        r"""
        while 1 [pr 4]
        """,
        TypeError,
    ],
}

#############################################################################


import unittest
from contextlib import redirect_stdout
from io import StringIO


class TestInterpreter(unittest.TestCase):
    pass


def add_interpreter_tests():
    def _make_test(source, expected):
        def _test(self):
            actual = StringIO()
            try:
                with redirect_stdout(actual):
                    run(source)
            except Exception as e:
                self.fail("Exception: {}".format(e))
            self.assertEqual(expected, actual.getvalue())

        return _test

    for name, (source, expected) in COMMAND_TESTS.items():
        setattr(TestInterpreter, "test_{0}".format(name), _make_test(source, expected))


class TestParser(unittest.TestCase):
    pass


def add_parser_tests():
    def _make_test(source):
        def _test(self):
            try:
                with redirect_stdout(StringIO()):
                    parse(source)
            except Exception as e:
                self.fail("Exception: {}".format(e))

        return _test

    for name, source in PARSER_TESTS.items():
        setattr(TestParser, "test_{0}".format(name), _make_test(source))


class TestType(unittest.TestCase):
    pass


def add_typeCheck_tests():
    def _make_test(source, expected):
        def _test(self):
            self.assertRaises(expected, lambda: run(source))

        return _test

    for name, (source, expected) in TYPE_TESTS.items():
        setattr(TestType, "test_{0}".format(name), _make_test(source, expected))


if __name__ == "__main__":
    add_parser_tests()
    add_interpreter_tests()
    add_typeCheck_tests()
    unittest.main(exit=False)
