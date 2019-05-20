from _ast import Add, Sub, Mult, Div
from ast import parse
from inspect import getsource
from unittest import TestCase, main


class MutationTestCase(TestCase):
    method = TestCase.assertEqual
    mutations = {'add': Add(), 'sub': Sub(), 'mult': Mult(), 'div': Div()}

    def assertEqual(self, x, y, z):
        if x == y:
            print(f"{self._testMethodName} Sobreviveu a mutação")
        else:
            self.method(x, y, z)

    @classmethod
    def mutate(cls, func_to_mutate, muts):
        """Mutate a function in scope."""

        def inner(func):
            def _inner(*args, **kwargs):
                for mutation in muts:
                    ast_module = parse(getsource(func_to_mutate))
                    ast_module.body[0].body[0].value.op = cls.mutations[mutation]
                    eval(
                        compile(ast_module, filename="<ast>", mode="exec"),
                        globals(),
                    )
                    func(*args, **kwargs)

            return _inner

        return inner


def soma(x, y):
    return x + y


class TestSoma(MutationTestCase):
    @MutationTestCase.mutate(soma, ['mult', 'sub'])
    def test_soma_deve_retornar_1(self):  # NOQA
        self.assertEqual(soma(0, 0), 0, "Deu ruim")


if __name__ == '__main__':
    main()
