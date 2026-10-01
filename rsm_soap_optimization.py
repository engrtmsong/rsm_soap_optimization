"""
Response Surface Methodology (RSM) Analysis:
Optimization of Soap Production from Balanites aegyptiaca Seed Oil

This project replicates, in Python, the statistical optimization
methodology used in my undergraduate thesis (Design-Expert software),
where I applied Design of Experiments (DoE) and Response Surface
Methodology to optimize three process variables:

    X1 = Reaction Temperature (deg C)
    X2 = NaOH Concentration (%)
    X3 = Reaction Time (minutes)

against the response:

    Y = Soap Yield (%)

IMPORTANT DATA NOTE (read this before using/citing this project):
The raw experimental data points from the original thesis were recorded
in Design-Expert and are not reproduced here. The dataset below is a
REPRESENTATIVE Central Composite Design (CCD) with a realistic response
surface (built to show the same curvature/optimum behaviour reported in
the thesis - yield rising with temperature and NaOH concentration up to
a point, then declining). This is a methodology demonstration, not a
republication of the original dataset. If you want this project to be
fully authentic, swap REPLACE_WITH_REAL_DATA below with your actual
thesis data table and rerun - the rest of the pipeline works unchanged.

Author: Abdullahi Mohammed
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from scipy import stats
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

np.random.seed(42)

# ---------------------------------------------------------------
# 1. BUILD THE CENTRAL COMPOSITE DESIGN (3 factors, face-centered)
# ---------------------------------------------------------------
# Coded levels: -1, 0, +1 (face-centered CCD, alpha = 1)
# Real ranges chosen to be realistic for saponification reactions
T_range   = (50, 80)    # Temperature, deg C
NaOH_range = (10, 20)   # NaOH concentration, %
time_range = (30, 90)   # Reaction time, minutes

def coded_to_real(coded, lo, hi):
    mid = (lo + hi) / 2
    half = (hi - lo) / 2
    return mid + coded * half

# Factorial points (2^3 = 8), axial points (6), center points (6 replicates)
factorial = [(-1,-1,-1),(1,-1,-1),(-1,1,-1),(1,1,-1),
             (-1,-1,1),(1,-1,1),(-1,1,1),(1,1,1)]
axial = [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]
center = [(0,0,0)] * 6

design_coded = factorial + axial + center
df = pd.DataFrame(design_coded, columns=["T_coded", "NaOH_coded", "time_coded"])
df["Temperature_C"] = coded_to_real(df["T_coded"], *T_range)
df["NaOH_percent"]  = coded_to_real(df["NaOH_coded"], *NaOH_range)
df["Time_min"]      = coded_to_real(df["time_coded"], *time_range)

# ---------------------------------------------------------------
# 2. GENERATE A REPRESENTATIVE RESPONSE (REPLACE_WITH_REAL_DATA)
# ---------------------------------------------------------------
# A quadratic surface with a realistic interior optimum, plus small
# random noise to emulate experimental error.
x1, x2, x3 = df["T_coded"], df["NaOH_coded"], df["time_coded"]
true_yield = (
    78
    + 2.5*x1 + 2.2*x2 + 0.9*x3
    - 3.1*x1**2 - 2.6*x2**2 - 1.4*x3**2
    + 1.2*x1*x2 - 0.6*x1*x3 + 0.4*x2*x3
)
noise = np.random.normal(0, 0.6, size=len(df))
df["Soap_Yield_percent"] = np.round(true_yield + noise, 2)

df.to_csv("outputs/design_and_results.csv", index=False)

# ---------------------------------------------------------------
# 3. FIT THE FULL QUADRATIC RSM MODEL
# ---------------------------------------------------------------
X = df[["T_coded", "NaOH_coded", "time_coded"]].values
y = df["Soap_Yield_percent"].values

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
feature_names = poly.get_feature_names_out(["T", "NaOH", "time"])

model = LinearRegression()
model.fit(X_poly, y)
y_pred = model.predict(X_poly)

# R-squared and adjusted R-squared
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - np.mean(y))**2)
r2 = 1 - ss_res/ss_tot
n, p = X_poly.shape
adj_r2 = 1 - (1-r2)*(n-1)/(n-p-1)

# Coefficient significance (t-test) via OLS standard errors
X_design = np.column_stack([np.ones(n), X_poly])
beta = np.linalg.lstsq(X_design, y, rcond=None)[0]
residuals = y - X_design @ beta
mse = np.sum(residuals**2) / (n - X_design.shape[1])
cov_beta = mse * np.linalg.inv(X_design.T @ X_design)
se_beta = np.sqrt(np.diag(cov_beta))
t_stats = beta / se_beta
p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), df=n - X_design.shape[1]))

coef_table = pd.DataFrame({
    "term": ["Intercept"] + list(feature_names),
    "coefficient": beta,
    "p_value": p_values
})
coef_table["significant_at_0.05"] = coef_table["p_value"] < 0.05
coef_table.to_csv("outputs/model_coefficients.csv", index=False)

with open("outputs/model_summary.txt", "w") as f:
    f.write("RSM QUADRATIC MODEL SUMMARY\n")
    f.write("=" * 40 + "\n")
    f.write(f"R-squared:          {r2:.4f}\n")
    f.write(f"Adjusted R-squared: {adj_r2:.4f}\n")
    f.write(f"Model p-value (overall F-test significance reflected in\n")
    f.write(f"term-level p-values below; model is significant if key\n")
    f.write(f"linear/quadratic terms have p < 0.05)\n\n")
    f.write(coef_table.to_string(index=False))

print("R-squared:", round(r2, 4), "| Adjusted R-squared:", round(adj_r2, 4))
print(coef_table.to_string(index=False))

# ---------------------------------------------------------------
# 4. FIND OPTIMUM CONDITIONS (maximize predicted yield)
# ---------------------------------------------------------------
def neg_yield(coded_vars):
    x = poly.transform([coded_vars])
    return -model.predict(x)[0]

result = minimize(neg_yield, x0=[0,0,0], bounds=[(-1,1)]*3, method="L-BFGS-B")
opt_coded = result.x
opt_yield = -result.fun

opt_real = {
    "Temperature_C": round(coded_to_real(opt_coded[0], *T_range), 1),
    "NaOH_percent":  round(coded_to_real(opt_coded[1], *NaOH_range), 2),
    "Time_min":      round(coded_to_real(opt_coded[2], *time_range), 1),
    "Predicted_Yield_percent": round(opt_yield, 2)
}
with open("outputs/optimum_conditions.txt", "w") as f:
    for k, v in opt_real.items():
        f.write(f"{k}: {v}\n")

print("\nOptimum conditions:", opt_real)

# ---------------------------------------------------------------
# 5. RESPONSE SURFACE AND CONTOUR PLOTS (Temperature x NaOH, time held at optimum)
# ---------------------------------------------------------------
t_grid = np.linspace(-1, 1, 40)
n_grid = np.linspace(-1, 1, 40)
Tg, Ng = np.meshgrid(t_grid, n_grid)
grid_points = np.column_stack([Tg.ravel(), Ng.ravel(), np.full(Tg.size, opt_coded[2])])
Z = model.predict(poly.transform(grid_points)).reshape(Tg.shape)

Tg_real = coded_to_real(Tg, *T_range)
Ng_real = coded_to_real(Ng, *NaOH_range)

fig = plt.figure(figsize=(14, 6))

ax1 = fig.add_subplot(1, 2, 1, projection="3d")
surf = ax1.plot_surface(Tg_real, Ng_real, Z, cmap="viridis", edgecolor="none", alpha=0.9)
ax1.set_xlabel("Temperature (deg C)")
ax1.set_ylabel("NaOH Concentration (%)")
ax1.set_zlabel("Predicted Soap Yield (%)")
ax1.set_title("3D Response Surface\n(Time held at optimum)")
fig.colorbar(surf, ax=ax1, shrink=0.6, label="Yield (%)")

ax2 = fig.add_subplot(1, 2, 2)
cont = ax2.contourf(Tg_real, Ng_real, Z, levels=20, cmap="viridis")
ax2.contour(Tg_real, Ng_real, Z, levels=10, colors="white", linewidths=0.5)
ax2.scatter(opt_real["Temperature_C"], opt_real["NaOH_percent"],
            color="red", marker="*", s=200, label="Predicted optimum", zorder=5)
ax2.set_xlabel("Temperature (deg C)")
ax2.set_ylabel("NaOH Concentration (%)")
ax2.set_title("Contour Plot of Soap Yield (%)")
ax2.legend()
fig.colorbar(cont, ax=ax2, label="Yield (%)")

plt.tight_layout()
plt.savefig("outputs/response_surface_and_contour.png", dpi=150)
print("\nPlots saved to outputs/response_surface_and_contour.png")
