import streamlit as st
from pathlib import Path

from src.simulation.GPS_data import CSVData
from src.simulation.battery_pack import BatteryPack, LiPo_SoC, LiPo_UoC, NMC_SoC, NMC_UoC
from src.simulation.battery_simulation import BatterySimulation


BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / "src" / "CSV_file" / "final_project_input_data.csv"

st.title("E-Bike Akku Simulation")

st.write("Hier kann eine GPS-Datei ausgewertet und der Akkuverbrauch simuliert werden.")

akku_typ = st.selectbox("Akkutyp auswaehlen", ["LiPo", "NMC"])

cell_capacity_Ah = st.number_input("Zellkapazitaet in Ah", value=3)
cells_series = 10
cells_parallel = st.number_input("Zellen parallel", value=6, min_value=1, step=1)


start = st.button("Simulation starten")


if start:
    # Akkus werden erstellt
    capacity_nom_Ah = cell_capacity_Ah * cells_parallel

    if akku_typ == "LiPo":
        internal_resistance_mOhm = cells_series * 8.0 / cells_parallel
        soc_points = LiPo_SoC
        ocv_points = LiPo_UoC
    else:
        internal_resistance_mOhm = cells_series * 7.0 / cells_parallel
        soc_points = NMC_SoC
        ocv_points = NMC_UoC

    akku = BatteryPack(
        capacity_nom_Ah=capacity_nom_Ah,
        internal_resistance_mOhm=internal_resistance_mOhm,
        initial_soc=1.0,
        Vmin=32.0,
        Vmax=42.0,
        soc_points=soc_points,
        ocv_points=ocv_points,
    )

    # CSV Daten werden eingelesen und bearbeitet
    gps_data = CSVData(CSV_FILE)
    summary = gps_data.summary()

    simulation = BatterySimulation(gps_data, akku)
    results = simulation.run()

    st.session_state.summary = summary
    st.session_state.results = results
    st.session_state.gps_data = gps_data


if "results" in st.session_state:
    st.success("Simulation abgeschlossen.")
    
    st.subheader("Route")
    route = st.session_state.gps_data.data[["lat", "lon"]]
    st.map(route)
    
    
    st.write("Tourdaten:")
    st.dataframe(st.session_state.summary)