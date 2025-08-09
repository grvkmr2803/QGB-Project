import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict

from qiskit_aer import AerSimulator
import mthree

from circuits.galton_circuit import build_qgb_circuit
from simulation.noisy_model import create_simple_noise_model

def calculate_variance(counts: Dict[str, int]) -> float:
    
    shots = sum(counts.values())
    if shots == 0: return 0
    bins = []
    for bitstring, count in counts.items():
        try:
            bin_index = bitstring.rfind('1')
            if bin_index != -1:
                bins.extend([bin_index] * count)
        except AttributeError:
            pass
    return np.var(bins) if bins else 0


if __name__ == "__main__":
    N_LAYERS = 4
    SHOTS = 8192

    
    ideal_sim = AerSimulator()

    noise_model = create_simple_noise_model()
    noisy_backend = AerSimulator(noise_model=noise_model)

    
    qgb_circuit = build_qgb_circuit(N_LAYERS, theta=np.pi / 2, add_measurements=True)
    qubits = list(range(1, qgb_circuit.num_qubits, 2))
    
    mitigator = mthree.M3Mitigation(noisy_backend)
    mitigator.cals_from_system(qubits)

    
    ideal_counts = ideal_sim.run(qgb_circuit, shots=SHOTS).result().get_counts()
    ideal_variance = calculate_variance(ideal_counts)

    noisy_job = noisy_backend.run(qgb_circuit, shots=SHOTS)
    noisy_counts = noisy_job.result().get_counts()
    noisy_variance = calculate_variance(noisy_counts)

    
    mitigated_qp = mitigator.apply_correction(noisy_counts, qubits)
    shots = 8192 
    mitigated_probs = mitigated_qp.nearest_probability_distribution()
    mitigated_counts = {state: int(prob * shots) for state, prob in mitigated_probs.items()}

    mitigated_variance = calculate_variance(mitigated_counts)

    
    theoretical_variance = N_LAYERS / 4

    
    print(f"Theoretical (Ideal) Variance:   {theoretical_variance:.4f}")
    print(f"Noiseless Simulation Variance:  {ideal_variance:.4f}")
    print(f"Raw Noisy Simulation Variance:  {noisy_variance:.4f}")
    print(f"Mitigated Simulation Variance:  {mitigated_variance:.4f}")

    labels = ['Theoretical', 'Noiseless Sim', 'Raw Noisy', 'Mitigated']
    variances = [theoretical_variance, ideal_variance, noisy_variance, mitigated_variance]
    colors = ['#4CAF50', '#2196F3', '#F44336', '#FFC107']

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, variances, color=colors)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.4f}', va='bottom')

    plt.ylabel('Variance')
    plt.title('Comparison of Variances with Measurement Error Mitigation')
    plt.savefig("report/plots/variance_comparison.png")
    plt.show()
