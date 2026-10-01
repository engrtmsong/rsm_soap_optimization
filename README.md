# RSM Optimization of Soap Production from *Balanites aegyptiaca* Seed Oil

A Python re-implementation of the Response Surface Methodology (RSM) and
Design of Experiments (DoE) approach used in my undergraduate thesis,
where I optimized soap production from a non-edible, locally sourced
desert date seed oil.

## Background

My thesis investigated *Balanites aegyptiaca* seed oil as a sustainable,
non-edible feedstock for soap production, using Design-Expert software to
apply DoE/RSM and develop a statistically validated predictive model
(p < 0.05) linking three process variables to soap yield.

This project rebuilds that same statistical methodology from first
principles in Python, without relying on commercial DoE software, to
demonstrate the underlying statistics and make the method fully
reproducible and inspectable.

## ⚠️ Data note (read this first)

The original thesis data was recorded in Design-Expert during laboratory
work and is not reproduced here. The dataset in this repository is a
**representative Central Composite Design (CCD)** built to reproduce the
same kind of curvature and interior optimum reported in the thesis — it
is a **methodology demonstration**, not a republication of the original
experimental results. Anyone wanting to verify the literal thesis values
should refer to the thesis manuscript itself.

The pipeline is written so that swapping in a real dataset (same column
structure) reproduces the full analysis unchanged — see
`rsm_soap_optimization.py`, the clearly marked data-generation section.

## Method

1. **Design construction** — a face-centered Central Composite Design
   (3 factors, 8 factorial points, 6 axial points, 6 center-point
   replicates) built manually with NumPy, covering:
   - Reaction Temperature: 50–80 °C
   - NaOH Concentration: 10–20%
   - Reaction Time: 30–90 minutes
2. **Model fitting** — a full quadratic response surface model
   (linear + quadratic + two-factor interaction terms) fitted with
   scikit-learn's `PolynomialFeatures` + `LinearRegression`.
3. **Statistical significance** — coefficient standard errors, t-statistics,
   and p-values computed directly via OLS theory (no black-box library),
   so every number in `outputs/model_coefficients.csv` can be traced back
   to the underlying linear algebra.
4. **Optimization** — `scipy.optimize.minimize` locates the stationary
   point of the fitted surface to identify optimal process conditions.
5. **Visualization** — 3D response surface and 2D contour plots showing
   the predicted yield landscape and marking the optimum.

## Results (on the representative dataset)

- R² = 0.993, Adjusted R² = 0.986 — all linear, quadratic, and
  interaction terms significant at p < 0.05, consistent with the
  thesis's reported model significance
- Predicted optimum: **74.7°C, 18.6% NaOH, 67 minutes → 79.3% predicted yield**

See `outputs/model_summary.txt` and `outputs/response_surface_and_contour.png`
for full results.

## Repository structure

```
rsm_soap_optimization.py       # full analysis pipeline, single script
outputs/
  design_and_results.csv       # the CCD design matrix and responses
  model_coefficients.csv       # fitted coefficients with p-values
  model_summary.txt            # R², adjusted R², full coefficient table
  optimum_conditions.txt       # predicted optimal process conditions
  response_surface_and_contour.png
README.md
```

## Running it yourself

```bash
pip install numpy pandas scikit-learn scipy matplotlib
python rsm_soap_optimization.py
```

## Author

Abdullahi Mohammed — B.Eng. Chemical Engineering, Modibbo Adama University,
Yola. [LinkedIn](https://www.linkedin.com/in/mohammed-abdullahi-a48a272a5)
