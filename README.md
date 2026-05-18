# LBBD for Flexible Job Shop Scheduling

A Logic-Based Benders Decomposition (LBBD) framework for the Flexible Job Shop Scheduling Problem (FJSP), built entirely with open-source solvers.

## Overview

The FJSP assigns operations to machines (where each operation has multiple machine options) and sequences them to minimise makespan. This project decomposes the problem using LBBD:

- **Master Problem (MIP):** Assigns operations to machines - solved with PySCIPOpt
- **Sub-Problem (CP):** Schedules operations on each machine - solved with OR-Tools CP-SAT
- **Benders Cuts:** Feasibility and optimality cuts drive convergence

A monolithic CP-SAT baseline is included for comparison.

## Project Structure

```
├── data/                # FJSP benchmark instances (JSON) from FJSPLib
├── benchmark_results/   # Best-known solutions for comparison
├── src/
│   ├── parser.py        # Instance parser
│   ├── baseline.py      # Monolithic CP-SAT solver
│   ├── master.py        # LBBD master problem (SCIP)
│   ├── subproblem.py    # LBBD sub-problem (CP-SAT)
│   ├── cuts.py          # Benders cut generation
│   ├── solver.py        # LBBD main loop
│   ├── validator.py     # Solution feasibility checker
│   └── visualise.py     # Gantt chart visualisation
├── results/             # Benchmark results
├── requirements.txt
└── README.md
```

## Benchmarks

Instances from [FJSPLib](https://scheduleopt.github.io/benchmarks/fjsplib) including Brandimarte, Fattahi, Kacem, and others.

## Installation

# Make the local environment.
```bash
python -m venv .venv
```

# Install the requirements.
```bash
pip install -r requirements.txt
```

## Usage


## Tech Stack

- **PySCIPOpt** - MIP master problem
- **OR-Tools CP-SAT** - CP sub-problem and monolithic baseline
- **Matplotlib** - Gantt chart visualisation
- **Python 3.10+**

## References

- Hooker, J.N. (2007). *Planning and Scheduling by Logic-Based Benders Decomposition.*
- Oddi et al. (2023). *Logic-based Benders Decomposition for preemptive Flexible Job-Shop Scheduling.*
- Benchmark instances from [FJSPLib](https://scheduleopt.github.io/benchmarks/fjsplib).

## Licence

Code: MIT
Benchmark data: [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) - sourced from [ScheduleOpt/benchmarks](https://github.com/ScheduleOpt/benchmarks)