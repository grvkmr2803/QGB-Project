import numpy as np
import matplotlib.pyplot as plt

from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from circuits.galton_circuit import build_qgb_circuit
from simulation.distance_metrics import calculate_tvd, calculate_js_divergence
from simulation.noisy_model import create_simple_noise_model


if __name__ == "__main__":
    SHOTS = 4096
    max_layers = 7
    
    theta = np.pi / 2  

    js_divergences = []
    tv_distances = []

    ideal_sim = AerSimulator()
    noise_model = create_simple_noise_model()

   

    for n in range(1, max_layers + 1):
       
        qc = build_qgb_circuit(n, theta)
       
        ideal_result = ideal_sim.run(qc, shots=SHOTS).result()
        counts_ideal = ideal_result.get_counts()
       
        noisy_result = ideal_sim.run(qc, shots=SHOTS, noise_model=noise_model).result()
        counts_noisy = noisy_result.get_counts()
       
        jsd = calculate_js_divergence(counts_ideal, counts_noisy, SHOTS)
        tvd = calculate_tvd(counts_ideal, counts_noisy, SHOTS)

        js_divergences.append(jsd)
        tv_distances.append(tvd)

       
    layers = list(range(1, max_layers + 1))
    plt.figure(figsize=(12, 7))
    plt.plot(layers, js_divergences, 'o-', label="Jensen-Shannon Divergence", color="dodgerblue")
    plt.plot(layers, tv_distances, 's-', label="Total Variation Distance", color="crimson")
    plt.title("Noise Impact vs. Circuit Depth", fontsize=16)
    plt.xlabel("Number of Layers", fontsize=12)
    plt.ylabel("Divergence from Ideal", fontsize=12)
    plt.xticks(layers)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("report/plots/noise_vs_depth.png") 
    plt.show()