A Streamlit-based Beam Analyzer for structural analysis with SFD & BMD visualization.
 ## Beam Analyser
An interactive web application for analyzing and visualizing statically determinate beams under various loading and support conditions.

#**Overview**
1] Analyze beams with multiple supports (fixed, pinned, roller).
2] Apply multiple types of loads: point loads, moments, UDLs, and linearly varying loads.
3] Compute reaction forces, shear force diagrams (SFD), and bending moment diagrams (BMD).
4] Visualize the beam geometry, support locations, and loading distribution.
5] Display key points such as maximum SFD and BMD values.

#**Features**
1] **Multiple Load Types:** Point loads, point moments (clockwise/anticlockwise), UDLs, and           triangular loads
2] **Support Types:** Fixed, pinned, and roller supports at any position along the beam 
3] **Automatic Reaction Calculation:** Solves equilibrium equations for all reaction forces
4] **Graphical Visualization:** Displays detailed beam diagram, SFD, and BMD with labeled maximum     values.
5] **Interactive Input:** Enter custom beam length, support locations, and load magnitudes
6] **Output:** It shows reaction forces and SFD, BMD diagrams.

#**Engineering Principles**
**Static equilibrium**
For statically determinate beams force in x-direction, y-direction and momentum is equal to zero.
The program automatically satisfies these equations to determine all reaction components.

#**Types of Supports**
1] **Fixed support** provides 1 vertical, 1 horizontal and 1 moment force
2] **Pinned support** provides 1 vertical, 1 horizontal rection forces.
3] ** Roller support** provides 1 vertical force.

#**Types of loads**
This web can take any number of Point loads, Point moments, UDL and Triangular loads.

#**Technologies Used**
1] **Python** programming
2] **Streamlit** for web interface
3] **NumPy** for numerical computation
4] **Matplotlib** for plotting SFD and BMD

#**Setup and Running**
1] Clone this repository
git clone https://github.com/tejasripalli0-cmyk/beam_analyser.git
cd beam_analyser
2] Install dependencies
pip install streamlit numpy matplotlib
3] Run the Streamlit app
streamlit run BeamAnalyzerApp.py
4] Access the application at
http://localhost:8501/

#**Usage Guide** 
1] Enter beam length and number of supports
2] Define each support type and position
3] Add loads (point, moment, UDL, or triangular)
4] Click **“Run Analysis”**
5] View results: Reaction forces, Beam Diagram, SFD, and BMD.
6] observe labeled points for maximum shear and bending moment values.

#**License**
MIT 
