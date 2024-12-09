import ast

print = __builtins__.print
exec = __builtins__.exec

del __builtins__

def santai():
  print("Santai bang, gak usah buru-buru")

class Santai(ast.NodeTransformer):
  def visit_Call(self, node: ast.Call) -> ast.AST:
    return ast.Call(func=ast.Name(id='santai', ctx=ast.Load()), args=[], keywords=[])
  
  def visit_Import(self, node: ast.AST) -> ast.AST:
    return ast.Expr(value=ast.Call(func=ast.Name(id='santai', ctx=ast.Load()), args=[], keywords=[]))
  
  def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.AST:
    return ast.Expr(value=ast.Call(func=ast.Name(id='santai', ctx=ast.Load()), args=[], keywords=[]))
  
  def visit_Assign(self, node: ast.Assign) -> ast.AST:
    return ast.Assign(targets=node.targets, value=ast.Constant(value=0))
  
  def visit_BinOp(self, node: ast.BinOp) -> ast.AST:
    return ast.BinOp(left=ast.Constant(0), op=node.op, right=ast.Constant(0))
  
  def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.AST:
    return ast.AnnAssign(target=node.target, annotation=node.annotation, value=ast.Constant(0))
  
  def visit_Attribute(self, node: ast.Attribute) -> ast.AST:
    if "self" in node.attr:
      return ast.Attribute(value=node.value, attr='__name__', ctx=node.ctx)
    return node

code = input('Pekris? Santai dulu gak sih? ').splitlines()[0]

code = ast.parse(code)
code = Santai().visit(code)
ast.fix_missing_locations(code)

exec(compile(code, '', 'exec'), {'__builtins__': {}}, {'santai': santai})