# Quantum Galton Board: Simulation, Noise Analysis, and Error Mitigation

This project provides a comprehensive implementation and analysis of a Quantum Galton Board (QGB), based on the concepts presented in the paper "Universal Statistical Simulator" (arXiv:2202.01735). The goal is to simulate a quantum walk, analyze its performance degradation under a realistic noise model, and demonstrate the effectiveness of quantum error mitigation techniques to improve simulation accuracy.

## Key Features

- **Generalized Circuit Builder:** A robust algorithm that programmatically constructs a QGB circuit for any number of layers.
- **Customizable Distributions:** The circuit supports both standard binomial distributions (via Hadamard gates) and custom-skewed distributions using parameterized $R_x(\theta)$ gates.
- **Rigorous Validation:** The ideal simulation output is validated against the exact mathematical binomial formula to prove the circuit's correctness.
- **Realistic Noise Simulation:** A custom depolarizing noise model is used to simulate the effects of errors on a near-term quantum device.
- **Performance Analysis:** The project includes a detailed analysis of how simulation accuracy degrades as circuit depth increases, quantified using multiple statistical distance metrics (Jensen-Shannon Divergence and Total Variation Distance).
- **Advanced Error Mitigation:** Implements state-of-the-art Measurement Error Mitigation using Qiskit's `CorrelatedReadoutMitigator` to correct for readout errors and recover a more accurate result.


## Setup and Installation

To run this project, please follow these steps to create a dedicated Python environment.

1.  **Clone or download the repository.**

2.  **Create and activate a new Conda environment:**
    ```bash
    conda create --name qgb-env python=3.10
    conda activate qgb-env
3.  **Install the required libraries from the `requirements.txt` file:**
    ```bash
    pip install -r requirements.txt
    ``````

## Usage

All analysis scripts should be run from the **root directory** of the project (`QuantumGaltonBoard/`) to ensure the local modules are imported correctly.

### 1. Distribution Validation
This script runs ideal simulations to validate the circuit's correctness against the analytical formula and to visualize the different distributions.
```bash
python -m analysis.ideal_and_validation
2. Noise Impact Analysis
This script analyzes how the simulation's accuracy is impacted by noise as the circuit depth increases.

Bash

python -m analysis.noisy_simulation
3. Error Mitigation
This script runs the final, most advanced analysis, applying Measurement Error Mitigation to correct the noisy results and recover a more accurate value.

Bash

python -m analysis.error_mitigation
Core Dependencies
Qiskit

Qiskit Aer

Qiskit IBM Provider

Matplotlib

SciPy

NumPy