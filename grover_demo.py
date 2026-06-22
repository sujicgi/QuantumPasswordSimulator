from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile


def run_grover_demo(target):

    qc = QuantumCircuit(2, 2)

    # 중첩 생성
    qc.h(0)
    qc.h(1)

    # ------------------
    # Oracle
    # ------------------

    if target == "00":
        qc.x([0, 1])
        qc.cz(0, 1)
        qc.x([0, 1])

    elif target == "01":
        qc.x(0)
        qc.cz(0, 1)
        qc.x(0)

    elif target == "10":
        qc.x(1)
        qc.cz(0, 1)
        qc.x(1)

    elif target == "11":
        qc.cz(0, 1)

    # ------------------
    # Diffusion
    # ------------------

    qc.h([0, 1])
    qc.x([0, 1])

    qc.cz(0, 1)

    qc.x([0, 1])
    qc.h([0, 1])

    # 측정
    qc.measure([0, 1], [0, 1])

    simulator = AerSimulator()

    compiled = transpile(
        qc,
        simulator
    )

    result = simulator.run(
        compiled,
        shots=1000
    ).result()

    qc.draw(
    output="mpl",
    filename="grover_circuit.png"
    )

    return result.get_counts()
