import numpy as np

def generate_helix_nec(filename, freq_mhz, mode='short'):
    c = 3e8
    wavelength = c / (freq_mhz * 1e6)

    if mode == 'short':
        a = wavelength / 40
        S = a
        N = 5
    elif mode == 'long':
        a = wavelength / (2 * np.pi)
        pitch_angle_deg = 13
        pitch_angle_rad = np.radians(pitch_angle_deg)
        S = 2 * np.pi * a * np.tan(pitch_angle_rad) / (2 * np.pi)
        N = 10
    else:
        raise ValueError("mode must be 'short' or 'long'")

    wire_radius = 0.001  # 1 mm wire
    segments_per_turn = 10
    total_segments = N * segments_per_turn
    L = S * N

    theta = np.linspace(0, 2 * np.pi * N, total_segments)
    x = a * np.cos(theta)
    y = a * np.sin(theta)
    z = np.linspace(0, L, total_segments)

    with open(filename, 'w') as f:
        f.write(f"CM {mode.title()} Helix Antenna @ {freq_mhz} MHz\n")
        f.write("CE\n")
        tag = 1
        for i in range(total_segments - 1):
            f.write(f"GW {tag} 1 {x[i]:.5f} {y[i]:.5f} {z[i]:.5f} {x[i+1]:.5f} {y[i+1]:.5f} {z[i+1]:.5f} {wire_radius:.5f}\n")
            tag += 1

        f.write("GE 0\n")
        f.write(f"EX 0,1,{total_segments//2},0,1.,0.\n")
        f.write(f"FR 0,1,0,0,{freq_mhz:.2f},0\n")
        f.write("RP 0,181,1,1000,0.,0.,1.,1.\n")
        f.write("EN\n")

# Generate .nec files
generate_helix_nec("short_helix.nec", freq_mhz=600, mode='short')
generate_helix_nec("long_helix.nec", freq_mhz=600, mode='long')
