import logging

import pandas as pd


class BatterySimulation:
    def __init__(self, gps_data, battery, current_column="engine_current", duration_column="delta_time"):
        self.gps_data = gps_data
        self.battery = battery
        self.current_column = current_column
        self.duration_column = duration_column

    def run(self):
        """In dieser Methode wird der Akku mit den GPS-Daten simuliert."""

        soc_values = []
        voltage_values = []

        for _, row in self.gps_data.data.iterrows():
            current = row[self.current_column]
            duration = row[self.duration_column]

            if pd.isna(current):
                current = 0.0

            if pd.notna(duration) and duration > 0 and not self.battery.is_empty():
                self.battery.apply_current(current=current, duration=duration)

            soc_values.append(self.battery.soc)
            voltage_values.append(self.battery.voltage(current=current))

        self.gps_data.data["battery_soc"] = soc_values
        self.gps_data.data["battery_soc_percent"] = self.gps_data.data["battery_soc"] * 100
        self.gps_data.data["battery_voltage"] = voltage_values

        logging.info("Akkusimulation wurde abgeschlossen.")

        return self.gps_data.data
