import matplotlib.pyplot as plt
# Step 1: Define constants and compute wavelength

c = 3e8  # speed of light in m/s
f = 900e6  # frequency in Hz (900 MHz)
wavelength = c / f  # in meters

print(f"Wavelength at 900 MHz: {wavelength:.3f} meters")

# Step 2: Calculate element lengths

reflector_length = 0.55 * wavelength
driven_length = 0.47 * wavelength
director_length = 0.45 * wavelength  # same length for all directors

print(f"Reflector Length: {reflector_length:.3f} m")
print(f"Driven Element Length: {driven_length:.3f} m")
print(f"Director Length: {director_length:.3f} m (same for all 3)")

# Step 3: Element positions along x-axis (start from reflector at x=0)

positions = {}
positions["Reflector"] = 0
positions["Driven"] = positions["Reflector"] + 0.2 * wavelength
positions["Director 1"] = positions["Driven"] + 0.15 * wavelength
positions["Director 2"] = positions["Director 1"] + 0.3 * wavelength
positions["Director 3"] = positions["Director 2"] + 0.3 * wavelength

# Display positions
for name, pos in positions.items():
    print(f"{name} position: {pos:.3f} m")

# Element lengths (in meters)
lengths = {
    "Reflector": reflector_length,
    "Driven": driven_length,
    "Director 1": director_length,
    "Director 2": director_length,
    "Director 3": director_length
}

# Plotting
fig, ax = plt.subplots()
for name, x_pos in positions.items():
    length = lengths[name]
    y_top = length / 2
    y_bottom = -length / 2
    ax.plot([x_pos, x_pos], [y_bottom, y_top], label=name, linewidth=3)

# Labels and styling
ax.set_title("Yagi–Uda Antenna Geometry @ 900 MHz (Top View)")
ax.set_xlabel("Position along x-axis (meters)")
ax.set_ylabel("Element length (meters)")
ax.legend()
ax.grid(True)
plt.axis('equal')
plt.show()

# Save Yagi-Uda antenna to NEC format

# Save Yagi-Uda antenna to NEC format

def generate_nec_file(filename, wavelength, positions, lengths, num_segments=11):
    with open(filename, 'w') as f:
        f.write("CM Yagi-Uda Antenna @ 900 MHz\n")
        f.write("CE\n")

        wire_id = 1
        radius = 0.001  # 1 mm wire radius

        for name, x in positions.items():
            length = lengths[name]
            y1 = -length / 2
            y2 = length / 2
            f.write(f"GW {wire_id} {num_segments} {x:.3f} {y1:.3f} 0 {x:.3f} {y2:.3f} 0 {radius:.4f}\n")
            wire_id += 1

        # Excitation (center segment of driven element, tag 2)
        f.write(f"EX 0 2 {num_segments//2+1} 0 1 0\n")

        # Frequency (1 freq point at 900 MHz)
        f.write("FR 0 1 0 0 900 0\n")

        # Radiation pattern (3D sweep)
        f.write("RP 0 181 1 1000 0 0 1 0\n")

        # End
        f.write("EN\n")

    print(f"NEC file '{filename}' generated.")

# Call the function
generate_nec_file("yagi_900mhz.nec", wavelength, positions, lengths)
