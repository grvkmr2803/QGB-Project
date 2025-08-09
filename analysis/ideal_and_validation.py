import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from circuits.galton_circuit import build_qgb_circuit


def get_prob_dist(counts, n_layers):
    total_shots = sum(counts.values())
    prob_dist = {i: 0 for i in range(n_layers + 1)}
    for bitstring, count in counts.items():
        try:
           
            bin_index = bitstring.rfind('1')
            if bin_index != -1:
                prob_dist[bin_index] += count / total_shots
        except AttributeError:
            pass
    return prob_dist

def get_analytical_dist(n_layers):
  
    probs = {}
    for k in range(n_layers + 1):
       
        probability = comb(n_layers, k) * (0.5**n_layers)
        probs[k] = probability
    return probs

if __name__ == "__main__":
   
    N_LAYERS = 6 
    SHOTS = 8192
    THETA_NORMAL = np.pi / 2   
    THETA_SKEWED = (2 * np.pi) / 3 

    
    ideal_sim = AerSimulator()

    qgb_normal = build_qgb_circuit(N_LAYERS, theta=THETA_NORMAL)
    counts_normal = ideal_sim.run(qgb_normal, shots=SHOTS).result().get_counts()
    
    qgb_skewed = build_qgb_circuit(N_LAYERS, theta=THETA_SKEWED)
    counts_skewed = ideal_sim.run(qgb_skewed, shots=SHOTS).result().get_counts()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    plot_histogram(counts_normal, ax=ax1, title=f"Normal Distribution ({N_LAYERS} Layers)", color='skyblue')
    plot_histogram(counts_skewed, ax=ax2, title=f"Skewed Distribution ({N_LAYERS} Layers)", color='salmon')
    fig.suptitle("Quantum Galton Board Ideal Simulation Results", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("report/plots/QGB_Ideal_simulation.png")
    plt.show()

    sim_probs = get_prob_dist(counts_normal, N_LAYERS)
    analytical_probs = get_analytical_dist(N_LAYERS)

    plt.figure(figsize=(12, 7))
    plt.bar(sim_probs.keys(), sim_probs.values(), label='Ideal Quantum Simulation', width=0.4, align='edge', color='dodgerblue')
    plt.bar(analytical_probs.keys(), analytical_probs.values(), label='Analytical Formula (Binomial)', width=-0.4, align='edge', color='orange')
    plt.title(f"Validation: Quantum Simulation vs. Analytical Formula ({N_LAYERS} Layers)", fontsize=16)
    plt.xlabel("Output Bin", fontsize=12)
    plt.ylabel("Probability", fontsize=12)
    plt.xticks(range(N_LAYERS + 1))
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("report/plots/Quantumsimulation_vs_anlytical.png")
    plt.show()