from qiskit_aer.noise import NoiseModel, errors

def create_simple_noise_model():
    noise_model = NoiseModel()

    p_meas = 0.15  
    p_gate = 0.05  
    p_cx = 0.10    

    meas_error = errors.readout_error.ReadoutError([[1 - p_meas, p_meas],
                                                    [p_meas, 1 - p_meas]])
    
    single_qubit_error = errors.depolarizing_error(p_gate, 1)
    two_qubit_error = errors.depolarizing_error(p_cx, 2)

    noise_model.add_all_qubit_readout_error(meas_error)

    noise_model.add_all_qubit_quantum_error(single_qubit_error, ['x', 'h', 'rx', 'ry', 'rz'])
    noise_model.add_all_qubit_quantum_error(two_qubit_error, ['cx'])

    return noise_model
