import numpy as np
import matplotlib.pyplot as plt
from scipy.signal.windows import chebwin

# Parameters
N = 32
d = 0.5
theta = np.linspace(0, np.pi, 1000)

# Centered element indices
n = np.arange(N) - (N - 1)/2

def array_factor(weights, theta, d, n):
    k = 2 * np.pi
    # outer over cos(theta) and element positions
    phase = np.exp(1j * k * d * np.outer(np.cos(theta), n))
    af = np.sum(weights * phase, axis=1)
    af /= np.max(np.abs(af))
    return 20 * np.log10(np.abs(af) + 1e-12)

# Plot everything together
plt.figure(figsize=(8, 5))
for sll, color in zip([20, 30, 40], ["C0", "C1", "C2"]):
    w = chebwin(N, at=sll, sym=True)
    af_db = array_factor(w, theta, d, n)
    plt.plot(np.degrees(theta), af_db, label=f"SLL = {sll} dB", color=color)

plt.title("Chebyshev Tapered Array Factor")
plt.xlabel("Angle (degrees)")
plt.ylabel("Normalized Array Factor (dB)")
plt.ylim(-60, 0)
plt.xlim(0, 180)
plt.grid(True)
plt.legend()
plt.show()
