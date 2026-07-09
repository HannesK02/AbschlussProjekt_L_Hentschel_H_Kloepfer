import streamlit as st

from src.figures import FigureCreator


st.title("Akkudaten")

if "results" not in st.session_state or "gps_data" not in st.session_state:
    st.warning("Bitte zuerst auf der Hauptseite die Simulation starten.")
else:
    raw_data = FigureCreator(st.session_state.gps_data.data)
    ergebnisse = FigureCreator(st.session_state.results)
    final_soc = st.session_state.results["battery_soc_percent"].iloc[-1]

    if final_soc <= 0:
        st.error("Der Akku hat zu wenig Kapazitaet fuer diese Strecke.")
    else:
        st.success(f"Am Ende der Strecke sind noch {final_soc:.1f} % Akkukapaziteat uebrig.")

    st.subheader("Akkustand")
    st.pyplot(ergebnisse.battery_soc())

    st.subheader("Akkuspannung")
    st.pyplot(ergebnisse.battery_voltage())

    st.subheader("Antriebsleistung")
    st.pyplot(raw_data.drive_power())

    st.subheader("Motorstrom")
    st.pyplot(raw_data.engine_current())
