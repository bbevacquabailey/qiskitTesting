from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator
 
qc = QuantumCircuit(2)
A = QuantumRegister(2)
C = ClassicalRegister(2)

qc.CX(0,1)
qc.h(0)

qc.measure(A, C)

