import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import matplotlib.pyplot as plt

from circuits.galton_circuit import build_qgb_circuit

circuit = build_qgb_circuit(n_layers=2, add_measurements=False)

fig = circuit.draw('mpl', fold=-1)
output_path = 'report/plots/circuit_diagram.png'
fig.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()
plt.close(fig) 
