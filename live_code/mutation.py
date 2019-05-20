from _ast import Add, Sub, Mult, Div
from ast import parse
from inspect import getsource

mutations = {
    'add': Add(),
    'sub': Sub(),
    'mult': Mult(),
    'div': Div(),
}


def mutate_with(mut, func_to_mutate):
    """Mutate a function in scope."""
    mutation = mutations[mut]

    def inner(func):
        def _inner(*args, **kwargs):
            ast_module = parse(getsource(func_to_mutate))
            ast_module.body[0].body[0].value.op = mutation
            eval(
                compile(ast_module, filename="<ast>", mode="exec"),
                globals(),
            )
            return func(*args, **kwargs)
        return _inner
    return inner
