import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Beam Analyzer", layout="wide")

st.title("Beam Analyzer")
st.write("Analyze beams with multiple supports and loads (point, UDL, or varying).")

# ------------------------
# 1. Beam Definition
# ------------------------
L = st.number_input("Enter beam length (m):", min_value=1.0, value=6.0, step=0.5)

# ------------------------
# 2. Support Input
# ------------------------
st.subheader("Supports")
num_supports = st.number_input("Number of supports:", min_value=2, max_value=5, value=2, step=1)
supports = []
support_types = ["Fixed", "Pinned", "Roller"]

for i in range(num_supports):
    col1, col2 = st.columns(2)
    with col1:
        pos = st.number_input(f"Position of Support {i+1} (m):", min_value=0.0, max_value=L, step=0.1, key=f"sup_pos{i}")
    with col2:
        stype = st.selectbox(f"Type of Support {i+1}:", support_types, key=f"sup_type{i}")
    supports.append((stype, pos))

# ------------------------
# 3. Load Input
# ------------------------
st.subheader("Loads")
num_loads = st.number_input("Number of loads:", min_value=0, max_value=10, value=1, step=1)
loads = []
load_types = ["Point Load", "Moment", "UDL", "Triangular Load"]

for i in range(num_loads):
    ltype = st.selectbox(f"Type of Load {i+1}:", load_types, key=f"load_type{i}")

    if ltype == "Point Load":
        P = st.number_input(f"Load {i+1} Magnitude (kN):", step=1.0, key=f"P{i}")
        a = st.number_input(f"Distance from left end (m):", step=0.1, key=f"a{i}")
        loads.append(("Point", P, a))

    elif ltype == "Moment":
        M = st.number_input(f"Moment {i+1} Magnitude (kN-m):", step=1.0, key=f"M{i}")
        a = st.number_input(f"Distance from left end (m):", step=0.1, key=f"Ma{i}")
        direction = st.selectbox(f"Direction of Moment {i+1}:", ["Clockwise", "Anticlockwise"], key=f"dir{i}")
        loads.append(("Moment", M, a, direction))

    elif ltype == "UDL":
        w = st.number_input(f"UDL {i+1} Intensity (kN/m):", step=0.5, key=f"w{i}")
        start = st.number_input(f"Start of UDL (m):", step=0.1, key=f"wstart{i}")
        end = st.number_input(f"End of UDL (m):", step=0.1, key=f"wend{i}")
        loads.append(("UDL", w, start, end))

    elif ltype == "Triangular Load":
        w1 = st.number_input(f"Start intensity (kN/m):", step=0.5, key=f"w1{i}")
        w2 = st.number_input(f"End intensity (kN/m):", step=0.5, key=f"w2{i}")
        start = st.number_input(f"Start of load (m):", step=0.1, key=f"tstart{i}")
        end = st.number_input(f"End of load (m):", step=0.1, key=f"tend{i}")
        loads.append(("Triangular", w1, w2, start, end))

# ------------------------
# 4. Analysis Button
# ------------------------
if st.button("Run Analysis"):
    st.subheader("Beam Diagram and Calculations")

    # Convert data to numpy arrays
    x = np.linspace(0, L, 400)
    V = np.zeros_like(x)
    M = np.zeros_like(x)

    # Simple reaction calculation for statically determinate beams (2 supports)
    if len(supports) == 2:
        A, B = supports[0][1], supports[1][1]
        RA, RB = 0, 0
        total_moment = 0
        total_vertical = 0

        for load in loads:
            if load[0] == "Point":
                P, a = load[1], load[2]
                total_vertical += P
                total_moment += P * (a - A)

            elif load[0] == "UDL":
                w, start, end = load[1], load[2], load[3]
                L_udl = end - start
                total_vertical += w * L_udl
                total_moment += w * L_udl * ((start + end) / 2 - A)

            elif load[0] == "Triangular":
                w1, w2, start, end = load[1], load[2], load[3], load[4]
                L_tri = end - start
                total_vertical += (w1 + w2) / 2 * L_tri
                centroid = (start + end) / 2  # approx
                total_moment += ((w1 + w2) / 2 * L_tri) * (centroid - A)

        RB = total_moment / (B - A)
        RA = total_vertical - RB
        st.write(f"Reactions: RA = {RA:.2f} kN, RB = {RB:.2f} kN")

        # Shear & Moment Calculation
        for load in loads:
            if load[0] == "Point":
                P, a = load[1], load[2]
                V[x >= a] -= P
                M[x >= a] -= P * (x[x >= a] - a)

            elif load[0] == "UDL":
                w, start, end = load[1], load[2], load[3]
                V[(x >= start) & (x <= end)] -= w * (x[(x >= start) & (x <= end)] - start)
                V[x > end] -= w * (end - start)
                M[(x >= start) & (x <= end)] -= (w / 2) * (x[(x >= start) & (x <= end)] - start) ** 2
                M[x > end] -= w * (end - start) * (x[x > end] - (start + end) / 2)

        V += RA * (x >= A)
        M += RA * (x - A) * (x >= A)
        M[x >= B] -= RB * (x[x >= B] - B)

        # ------------------------
        # Beam, SFD, BMD Plots
        # ------------------------
        fig, axs = plt.subplots(3, 1, figsize=(10, 10))

        # Beam diagram
        axs[0].axhline(0, color='black', lw=2)
        for s in supports:
            stype, pos = s
            if stype == "Fixed":
                axs[0].plot(pos, 0, 'ks', markersize=10, label='Fixed' if 'Fixed' not in axs[0].get_legend_handles_labels()[1] else "")
            elif stype == "Pinned":
                axs[0].plot(pos, 0, 'g^', markersize=10, label='Pinned' if 'Pinned' not in axs[0].get_legend_handles_labels()[1] else "")
            elif stype == "Roller":
                axs[0].plot(pos, 0, 'bo', markersize=10, label='Roller' if 'Roller' not in axs[0].get_legend_handles_labels()[1] else "")
        axs[0].set_xlim(0, L)
        axs[0].set_title("Beam Diagram")
        axs[0].legend()
        axs[0].grid(True)

        # SFD
        axs[1].plot(x, V, 'b', lw=2)
        axs[1].set_title("Shear Force Diagram (SFD)")
        axs[1].set_xlabel("Beam Length (m)")
        axs[1].set_ylabel("Shear Force (kN)")
        axs[1].grid(True)
        axs[1].text(x[np.argmax(np.abs(V))], V[np.argmax(np.abs(V))],
                    f"Max: {V[np.argmax(np.abs(V))]:.2f}", color='r')

        # BMD
        axs[2].plot(x, M, 'r', lw=2)
        axs[2].set_title("Bending Moment Diagram (BMD)")
        axs[2].set_xlabel("Beam Length (m)")
        axs[2].set_ylabel("Bending Moment (kN·m)")
        axs[2].grid(True)
        axs[2].text(x[np.argmax(np.abs(M))], M[np.argmax(np.abs(M))],
                    f"Max: {M[np.argmax(np.abs(M))]:.2f}", color='b')

        st.pyplot(fig)

    else:
        st.error("Currently supports more than 2 supports are under development for indeterminate beams.")
