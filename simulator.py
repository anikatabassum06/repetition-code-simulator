import numpy as np
import random
import matplotlib.pyplot as plt

# ─────────────────────────────────────────
# STEP 1: ENCODE
# ─────────────────────────────────────────
def encode(logical_qubit, n=3):
    return [logical_qubit] * n

# ─────────────────────────────────────────
# STEP 2: INJECT ERROR
# ─────────────────────────────────────────
def inject_error(encoded, error_prob=0.1):
    corrupted = encoded.copy()
    error_positions = []
    for i in range(len(encoded)):
        if random.random() < error_prob:
            corrupted[i] = 1 - corrupted[i]
            error_positions.append(i)
    return corrupted, error_positions

# ─────────────────────────────────────────
# STEP 3: MEASURE SYNDROME
# ─────────────────────────────────────────
def measure_syndrome(corrupted):
    syndromes = []
    for i in range(len(corrupted) - 1):
        syndromes.append(corrupted[i] ^ corrupted[i+1])
    return syndromes

# ─────────────────────────────────────────
# STEP 4: CORRECT
# ─────────────────────────────────────────
def correct(corrupted, syndromes):
    corrected = corrupted.copy()
    n = len(corrupted)

    # find which qubit is most likely flipped
    votes = [0] * n
    for i, s in enumerate(syndromes):
        if s == 1:
            votes[i]   += 1
            votes[i+1] += 1

    # flip the qubit with the most votes
    max_votes = max(votes)
    if max_votes > 0:
        error_qubit = votes.index(max_votes)
        corrected[error_qubit] = 1 - corrected[error_qubit]

    return corrected

# ─────────────────────────────────────────
# STEP 5: DECODE
# ─────────────────────────────────────────
def decode(corrected):
    return 1 if sum(corrected) > len(corrected) / 2 else 0

# ─────────────────────────────────────────
# STEP 6: RUN ONE FULL CYCLE
# ─────────────────────────────────────────
def run_once(logical_qubit, error_prob=0.1, n=3):
    encoded   = encode(logical_qubit, n)
    corrupted, error_positions = inject_error(encoded, error_prob)
    syndromes = measure_syndrome(corrupted)
    corrected = correct(corrupted, syndromes)
    decoded   = decode(corrected)
    return decoded == logical_qubit

# ─────────────────────────────────────────
# STEP 7: RUN SIMULATION + COMPARE PLOT
# ─────────────────────────────────────────
def run_simulation(trials=1000):
    error_probs = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]

    success_3 = []
    success_5 = []

    for ep in error_probs:
        # 3-qubit
        s3 = sum(run_once(random.randint(0,1), ep, n=3) for _ in range(trials))
        success_3.append(s3 / trials * 100)

        # 5-qubit
        s5 = sum(run_once(random.randint(0,1), ep, n=5) for _ in range(trials))
        success_5.append(s5 / trials * 100)

    # ── Plot ──
    plt.figure(figsize=(9, 6))
    plt.plot(error_probs, success_3, marker='o', color='royalblue',
             linewidth=2, label='3-qubit repetition code')
    plt.plot(error_probs, success_5, marker='s', color='crimson',
             linewidth=2, label='5-qubit repetition code')

    plt.title('Repetition Code — 3-qubit vs 5-qubit Correction Success Rate')
    plt.xlabel('Error Probability')
    plt.ylabel('Success Rate (%)')
    plt.ylim(0, 100)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('results_comparison.png')
    plt.show()
    print("Plot saved as results_comparison.png")

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 45)
    print("   3-QUBIT vs 5-QUBIT COMPARISON")
    print("=" * 45)
    run_simulation()