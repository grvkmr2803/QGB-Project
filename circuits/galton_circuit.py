import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import jensenshannon
from scipy.stats import norm
from qiskit import QuantumRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit import QuantumCircuit, ClassicalRegister


def calculate_js_divergence(counts1, counts2, shots):
    
    all_outcomes = sorted(list(set(counts1.keys()) | set(counts2.keys())))
    prob_dist1 = np.array([counts1.get(outcome, 0) / shots for outcome in all_outcomes])
    prob_dist2 = np.array([counts2.get(outcome, 0) / shots for outcome in all_outcomes])
    return jensenshannon(prob_dist1, prob_dist2) ** 2


def create_simple_noise_model():
    
    error_rate = 0.005
    one_qubit_error = depolarizing_error(error_rate, 1)
    two_qubit_error = depolarizing_error(error_rate, 2)
    three_qubit_error = depolarizing_error(error_rate, 3)

    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(one_qubit_error, ['u', 'h', 'rx', 'x', 'reset'])
    noise_model.add_all_qubit_quantum_error(two_qubit_error, ['cx'])
    noise_model.add_all_qubit_quantum_error(three_qubit_error, ['cswap'])
    return noise_model


def apply_peg_operator(qc, control_qubit, board_qubits):
    
    q_left, q_ball, q_right = board_qubits
    qc.cswap(control_qubit, q_left, q_ball)
    qc.cx(q_ball, control_qubit)
    qc.cswap(control_qubit, q_ball, q_right)



def build_qgb_circuit(n_layers, theta=None, add_measurements=True):
    
    num_board_qubits = 2 * n_layers + 1
    total_qubits = num_board_qubits + 1  
    
    qreg = QuantumRegister(total_qubits, "q")
    creg = ClassicalRegister(n_layers + 1, "c")
    qc = QuantumCircuit(qreg, creg)

    control_q = 0
    active_qubits = [n_layers + 1]
    qc.x(active_qubits[0])
    qc.barrier()

    for layer in range(n_layers):
        qc.reset(control_q)
        if theta is not None:
            qc.rx(theta, control_q)
        else:
            qc.h(control_q)

        next_active_qubits = []
        for i, ball_qubit in enumerate(active_qubits):
            peg_indices = [ball_qubit - 1, ball_qubit, ball_qubit + 1]
            apply_peg_operator(qc, control_q, peg_indices)
            next_active_qubits.extend([ball_qubit - 1, ball_qubit + 1])

            if i < len(active_qubits) - 1:
                qc.cx(peg_indices[2], control_q)

        active_qubits = sorted(list(set(next_active_qubits)))
        qc.barrier()

    if add_measurements:
        output_qubits = list(range(1, total_qubits, 2))
        for i, qubit_idx in enumerate(output_qubits):
            qc.measure(qubit_idx, creg[i])

    return qc



def fit_gaussian(counts, shots):
    
    outcomes = np.array([int(k, 2) for k in counts.keys()])
    probabilities = np.array([v / shots for v in counts.values()])

    mean, std = norm.fit(np.repeat(outcomes, (probabilities * shots).astype(int)))

    x = np.linspace(min(outcomes), max(outcomes), 100)
    fitted = norm.pdf(x, mean, std)
    plt.plot(x, fitted * sum(probabilities), label="Fitted Gaussian", linestyle='--')
    return mean, std



if __name__ == "__main__":
    N_LAYERS = 3
    SHOTS = 8192

    standard_qgb = build_qgb_circuit(N_LAYERS)

    ideal_sim = AerSimulator()
    custom_noise_model = create_simple_noise_model()

    job_ideal = ideal_sim.run(standard_qgb, shots=SHOTS)
    counts_ideal = job_ideal.result().get_counts()

    job_noisy = ideal_sim.run(standard_qgb, shots=SHOTS, noise_model=custom_noise_model)
    counts_noisy = job_noisy.result().get_counts()

    jsd = calculate_js_divergence(counts_ideal, counts_noisy, SHOTS)
    print(f"Jensen-Shannon Divergence between Ideal and Noisy: {jsd:.4f}")

    legend = ['Ideal (Simulator)', 'Noisy (Custom Model)']
    plot_histogram([counts_ideal, counts_noisy], legend=legend, figsize=(15, 7),
                   title=f"Ideal vs. Noisy Results for {N_LAYERS}-Layer Standard QGB")
    plt.savefig("report/plots/ideal_vs_noisy_standard_QGB.png")
    plt.show()

    mean, std = fit_gaussian(counts_ideal, SHOTS)
    plt.legend()
    plt.title(f"Fitted Gaussian: μ={mean:.2f}, σ={std:.2f}")
    plt.savefig("report/plots/Fitted_Gaussian.png")
    plt.show()
