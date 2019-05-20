from _ast import Add, Sub, Mult, Div
from ast import parse
from inspect import getsource


aor_mutations = [Add, Sub, Mult, Div]


def possible_mutations(op, mutations):
    return list(filter(lambda x: not isinstance(op, x), mutations))


def aor(func_to_mutate):
    original_code = getsource(func_to_mutate)
    ast_module = parse(original_code)

    def _aor(func):
        default_op = ast_module.body[0].body[0].value.op
        ops = possible_mutations(default_op, aor_mutations)

        def inner(*args, **kwargs):
            for mutation in ops:
                ast_module.body[0].body[0].value.op = mutation()
                eval(
                    compile(ast_module, filename="<ast>", mode="exec"),
                    globals(),
                )
                try:
                    func(*args, **kwargs)
                    print(f'SURVIVED {func.__name__}: {mutation}')
                except Exception as e:
                    print(f'PASSED {func.__name__}: {mutation}. ERROR: {e}')

        return inner
    return _aor


# =================================================
def soma(x, y):
    return x + y


@aor(soma)
def test_soma_0_0_deve_retornar_0():  # NOQA
    assert soma(0, 0) == 0


@aor(soma)
def test_soma_1_1_deve_retornar_2():  # NOQA
    assert soma(1, 1) == 2


@aor(soma)
def test_soma__1__1_deve_retornar__2():  # NOQA
    assert soma(-1, -1) == -2


test_soma_0_0_deve_retornar_0()
test_soma_1_1_deve_retornar_2()
test_soma__1__1_deve_retornar__2()
