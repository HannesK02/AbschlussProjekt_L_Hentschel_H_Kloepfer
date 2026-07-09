import streamlit as st

from src.figures import FigureCreator


st.title("Tourdaten")

if "gps_data" not in st.session_state:
    st.warning("Bitte zuerst auf der Hauptseite die Simulation starten.")
else:
    raw_data = FigureCreator(st.session_state.gps_data.data)

    st.subheader("Hoehenprofil")
    st.pyplot(raw_data.elevation_profile())

    st.subheader("Geschwindigkeit")
    st.pyplot(raw_data.velocity())
