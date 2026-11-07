# Response Surface Methodology for Soap Production from *Balanites aegyptiaca* Seed Oil

**Research-methods demonstration | Python | Design of Experiments | Chemical Engineering**

This repository illustrates how a quadratic response surface can be fitted and optimized in Python. It is inspired by my 2025 undergraduate thesis on soap production from *Balanites aegyptiaca* (desert date) seed oil at Modibbo Adama University, Yola, Nigeria.

## Research context

The undergraduate study investigated a locally available non-edible oil feedstock and applied Design of Experiments (DoE), Central Composite Design (CCD), and Response Surface Methodology (RSM) to investigate process conditions. The thesis used Design-Expert for its original experimental analysis.

**Research-integrity note:** The data in this GitHub script are **representative/synthetic demonstration data**, not the thesis's original measured observations. Consequently, numerical predictions from the script must not be cited as experimental findings or as independent validation of the thesis. The repository demonstrates the *method*, not reproduction of the original dataset.

## What the code demonstrates

- Constructing a three-factor CCD with NumPy
- Fitting a quadratic model with scikit-learn
- Computing model coefficient statistics
- Optimizing the fitted response using SciPy
- Plotting response surfaces and contour maps

## Run locally

```bash
python -m pip install numpy pandas scikit-learn scipy matplotlib
python rsm_soap_optimization.py
```

The script generates its analysis outputs when run. Generated output files are **not currently committed** to this repository; see the script for paths and assumptions. Check model fit and optimization constraints before interpreting results.

## Next research steps

1. With appropriate permission, replace demonstration data with a properly documented, anonymized experimental dataset.
2. Compare Python-derived statistics with the original Design-Expert analysis.
3. Add reproducibility checks, unit tests, and a data dictionary.
4. Document uncertainty and practical feasibility of any predicted optimum.

## Related academic work

- **2025 B.Eng. thesis:** Optimization of soap production from *Balanites aegyptiaca* seed oil using DoE/RSM.
- **2025 process plant design:** Conceptual design of a 100-tonne/day sodium bicarbonate plant using a Solvay-process route.
- **2019 diploma project:** Emulsion paint formulation using locally sourced materials.

These are separate academic projects; their full reports and original datasets are not automatically published here.

## Author

**Mohammed Abdullahi** — B.Eng. Chemical Engineering, Modibbo Adama University, Yola, Nigeria. Interested in process systems engineering, sustainable process design, statistical optimization and process simulation.

[LinkedIn](https://www.linkedin.com/in/mohammed-abdullahi-a48a272a5) · [X](https://x.com/EngrTMSong)
