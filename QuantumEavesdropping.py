from qiskit import transpile, QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector, DensityMatrix
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_multivector, plot_histogram
import numpy as np
import matplotlib.pyplot as plt
from plotBlochVectors import fidelity

n = 1

A = QuantumRegister(n, "A")
C = ClassicalRegister(n, "C")

shots = 10

theta = np.pi/2
phi = np.pi/2

qc = QuantumCircuit(A, C)

state = Statevector([
    np.cos(theta/2), 
    np.exp(1j* phi)*np.sin(theta/2)
]
)

qc.prepare_state(state)

plot_bloch_multivector(qc)

plt.show()

qc.measure(A, C)


backend = AerSimulator()
circ = transpile(qc, backend)
result = backend.run(circ, shots = shots).result()
compCounts = result.get_counts(circ)
plot_histogram(compCounts)
# plt.show()

qc = QuantumCircuit(A, C)

state = Statevector([
    np.cos(theta/2), 
    np.exp(1j* phi)*np.sin(theta/2)
]
)

qc.prepare_state(state)

for i in range(qc.num_qubits):
    qc.h(i)

qc.measure(A, C)

circ = transpile(qc, backend)
result = backend.run(circ, shots = shots).result()
hadCounts = result.get_counts(circ)
plot_histogram(hadCounts)

# plt.show()

qc = QuantumCircuit(A, C)

state = Statevector([
    np.cos(theta/2), 
    np.exp(1j* phi)*np.sin(theta/2)
]
)

qc.prepare_state(state)

for i in range(qc.num_qubits):
    qc.sdg(i)
    qc.h(i)

qc.measure(A, C)

circ = transpile(qc, backend)
result = backend.run(circ, shots = shots).result()
plexCounts = result.get_counts(circ)
plot_histogram(plexCounts)

# plt.show()

scomp = (compCounts.get('0', 0)/shots) - (compCounts.get('1', 0)/shots)
 
shad = (hadCounts.get('0', 0)/shots) - (hadCounts.get('1', 0)/shots)

splex = (plexCounts.get('0', 0)/shots) - (plexCounts.get('1', 0)/shots)


I = np.array([[1,0],[0,1]])
X = np.array([[0,1],[1,0]])
Y = np.array([[0,-1j],[1j,0]])
Z = np.array([[1,0],[0,-1]])

p = 1/2*(I + shad*X + splex*Y + scomp*Z)

eigenvalues, eigenvectors = np.linalg.eigh(p)

idx = np.argmax(eigenvalues)
psi = eigenvectors[:, idx]

print("Eigenvalues:", eigenvalues)
print("Statevector:", psi)

