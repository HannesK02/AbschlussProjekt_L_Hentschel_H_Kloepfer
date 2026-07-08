import streamlit as st
import matplotlib.pyplot as plt

from figures import FigureCreator
from simulation.GPS_data import CSVData
from simulation.battery_pack import BatteryPack, LiPo_SoC, LiPo_UoC, NMC_SoC, NMC_UoC
from simulation.battery_simulation import BatterySimulation

st.title("E-Bike Akku Simulation")

st.write("Hier kann eine GPS-Datei ausgewertet und der Akkuverbrauch simuliert werden.")

akku_typ = st.selectbox("Akkutyp auswählen", ["LiPo", "NMC"])

cell_capacity_Ah = st.number_input("Zellkapazität in Ah", value = 3)
cells_series = 10
cells_parallel = st.number_input("Zellen parallel", value= 6, min_value= 1, step= 1)


start = st.button("Simulation starten")


if start:

    #Akkus werden erstellt

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
        capacity_nom_Ah= capacity_nom_Ah,
        internal_resistance_mOhm=internal_resistance_mOhm,
        initial_soc=1.0,
        Vmin=32.0,
        Vmax=42.0,
        soc_points=soc_points,
        ocv_points=ocv_points,
        )   
    
    
    #CSV Daten werden eingelesen und bearbeitet

    gps_data = CSVData("src/CSV_file/final_project_input_data.csv")

    simulation = BatterySimulation(gps_data, akku)
    results = simulation.run()

    st.dataframe(results)

    figures = FigureCreator(results)
    st.pyplot(figures.battery_soc())
    st.pyplot(figures.battery_voltage())
