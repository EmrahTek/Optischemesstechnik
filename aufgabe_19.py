import sympy as sp

alpha, eps, c,x =sp.symbols('alpha eps c x', positive=True,real=True)

I_ratio =sp.exp(alpha*x)
E = sp.log(I_ratio,10)
expr = sp.Eq(E,eps*c*x)

alpha_expr = sp.solve(expr,alpha)[0]
sp.simplify(alpha_expr)
print(alpha_expr)