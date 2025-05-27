import numpy as np

def generate_helix_nec(filename, freq_mhz, mode='short'):
    c = 3e8
    freq_hz = freq_mhz * 1e6
    wavelength = c / freq_hz

    if mode == 'short':
        a = wavelength / 40  # small radius
        pitch = a            # spacing = a
        turns = 5
    elif mode == 'long':
        a = wavelength / (2 * np.pi)
        pitch_angle_deg = 13
        pitch_angle_rad = np.radians(pitch_angle_deg)
        pitch = 2 * np.pi * a * np.tan(pitch_angle_rad) / (2 * np.pi)  # simplifies to a * tan(angle)
        turns = 10
    else:
        raise ValueError("mode must be 'short' or 'long'")

    segments_per_turn = 10
    total_segments = turns * segments_per_turn
    wire_radius = 0.001  # 1 mm

    theta = np.linspace(0, 2 * np.pi * turns, total_segments)
    z = np.linspace(0, pitch * turns, total_segments)
    x = a * np.cos(theta)
    y = a * np.sin(theta)

    with open(filename, 'w') as f:
        f.write(f"CM {mode.title()} Helical Antenna @ {freq_mhz} MHz\n")
        f.write("CE\n")
        tag = 1
        for i in range(total_segments - 1):
            f.write(f"GW {tag} 1 {x[i]:.5f} {y[i]:.5f} {z[i]:.5f} {x[i+1]:.5f} {y[i+1]:.5f} {z[i+1]:.5f} {wire_radius:.5f}\n")
            tag += 1

        f.write("GE 0\n")

        # Feed at first segment
        f.write(f"EX 0,1,1,0,1.0,0.0\n")

        # Frequency
        f.write(f"FR 0,1,0,0,{freq_mhz:.2f},0\n")

        # Radiation pattern (full azimuth sweep at theta=90°)
        f.write("RP 0,361,1,1000,90.,0.,1.,1.\n")

        f.write("EN\n")

# Generate both modes
generate_helix_nec("short_helix.nec", freq_mhz=600, mode='short')
generate_helix_nec("long_helix.nec", freq_mhz=600, mode='long')
