import sympy as sp

#semboller
alpha, x = sp.symbols('alpha x', positive=True, real=True)

# Verilenler
T1 = sp.Rational(16,100) # 0.16 
x1 = 1.0 # mm 

# 1) Absorption für 1 mm
A1 = 1- T1
print("Absorption A1 = ", sp.N(A1)) # 0.84

# 2) Absroptionskoeffizient alpha aus T = exp(-alpha*x)
# T1 = exp(-alpha*x1)
eq_alpha = sp.Eq(T1,sp.exp(-alpha*x1))
alpha_sol = sp.solve(eq_alpha, alpha)[0]
print("alpha=", alpha_sol,"~", float(alpha_sol), "1/mm")

# 3) Transmission für 2 mm
x2 = 2.0  # mm
T2 = sp.exp(-alpha_sol * x2)
print("T2 =", sp.N(T2), "≈", float(T2))