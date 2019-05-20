import ast
import _ast
import inspect

funcao_soma = """
def soma(x, y):
    return x + y
"""

def soma(x, y):
    return x + y


# Modulo geral do parse
ast_module = ast.parse(funcao_soma)
# <_ast.Module at 0x7f3173b02710>

# Corpo do módulo
body = ast_module.body
# [<_ast.FunctionDef at 0x7f3173b02908>]

# Definição da função
func = body[0]
# <_ast.FunctionDef at 0x7f3173b02908>

# Corpo da função
f_body = func.body[0]
# <_ast.Return at 0x7f3173b02940>

# Valor da função
f_body.value
# <_ast.BinOp at 0x7f3173b02978>

# Operação da função
f_body.value.op
# <_ast.Add at 0x7f60a4339278>

exec(compile(ast_module, filename="<ast>", mode="exec"))

print(funcao_soma)

assert soma(1, 1) == 2

ast_module.body[0].body[0].value.op = _ast.Sub()

exec(compile(ast_module, filename="<ast>", mode="exec"))

inspect.getsource(soma)

assert soma(1, 1) == 2
