import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal.windows import chebwin

# 1) Array & angle setup
N = 32
d = 0.5             # element spacing (λ)
theta = np.linspace(0, np.pi, 1000)
angles_deg = np.degrees(theta)

# center the element indices for symmetry
n = np.arange(N) - (N - 1)/2

# 2) Define the four tapers
tapers = {
    "Uniform": np.ones(N),
    "Cheb 20 dB": chebwin(N, at=20, sym=True),
    "Cheb 30 dB": chebwin(N, at=30, sym=True),
    "Cheb 40 dB": chebwin(N, at=40, sym=True),
}

# 3) Array‐factor function
def array_factor_db(weights):
    k = 2 * np.pi
    phase = np.exp(1j * k * d * np.outer(np.cos(theta), n))
    af = np.abs(np.sum(weights * phase, axis=1))
    af /= np.max(af)
    return 20 * np.log10(af + 1e-12)

# 4) Compute & collect metrics
results = []
af_curves = {}
for name, w in tapers.items():
    af_db = array_factor_db(w)
    af_curves[name] = af_db

    # find indices around the main lobe to get the –3 dB beamwidth
    peak_idx = np.argmax(af_db)
    # walk left and right until AF drops below –3 dB
    left = peak_idx
    while left > 0 and af_db[left] >= -3:
        left -= 1
    right = peak_idx
    while right < len(af_db)-1 and af_db[right] >= -3:
        right += 1
    bw = angles_deg[right] - angles_deg[left]

    # sidelobe level: max in the regions outside [left, right]
    sidelobes = np.concatenate((af_db[:left], af_db[right:]))
    sll = -np.max(sidelobes)  # positive dB

    results.append({
        "Taper": name,
        "Beamwidth (°)": round(bw, 3),
        "SLL (dB)": round(sll, 3),
    })

# 5) Plot all four in one figure
plt.figure(figsize=(8, 4))
for name, af_db in af_curves.items():
    plt.plot(angles_deg, af_db, label=name)
plt.title("Array Factor Comparison")
plt.xlabel("Angle (°)")
plt.ylabel("Normalized AF (dB)")
plt.ylim(-60, 0)
plt.xlim(0, 180)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# 6) Print the results table
df = pd.DataFrame(results)
print(df.to_string(index=False))
