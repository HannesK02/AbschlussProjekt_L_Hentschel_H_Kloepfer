import pandas as pd
import numpy as np
import logging

class CSVData:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = pd.read_csv(csv_file)

        logging.info("CSV-Datei wurde eingelesen.")

        self.validate()
        self.prepare()
        self.sort_by_time()
        self.calculate_time_difference()
        self.calculate_distance()
        self.calculate_velocity()
        self.calculate_acceleration()
        self.calculate_gradient()
        


    def validate(self):
        """Diese Methode überprüft ob alle benötigten Spalten in der CSV-Datei sind."""

        required_columns = ["lat", "lon", "ele", "time"]

        for column in required_columns:
            if column not in self.data.columns:
                logging.error(f"Die Spalte {column} fehlt in der CSV-Datei.")
                raise ValueError(f"Die Spalte {column} fehlt in der CSV-Datei.")
            
        logging.info("Die CSV-Datei hat das richtige Format.")

    
    def prepare(self):
        """Diese Methode wandelt die Einträge in Zahlen um und entfernt Zeilen in denen ein Fehler ist."""

        self.data["lat"] = pd.to_numeric(self.data["lat"], errors="coerce")
        self.data["lon"] = pd.to_numeric(self.data["lon"], errors="coerce")
        self.data["ele"] = pd.to_numeric(self.data["ele"], errors="coerce")
        self.data["time"] = pd.to_datetime(self.data["time"], errors="coerce")

        rows_before = len(self.data)

        self.data = self.data.dropna(subset=["lat", "lon", "ele", "time"])

        rows_after = len(self.data)
        removed_rows = rows_before - rows_after

        if removed_rows > 0:
            logging.warning(f"{removed_rows} ungültige Zeilen wurden entfernt.")


        if len(self.data) < 2:
            logging.error("Die CSV-Datei enthält zu wenige gültige Zeilen.")
            raise ValueError("Die CSV-Datei enthält zu wenige gültige Zeilen.")

    def sort_by_time(self):
        """In der Mathode werden die Messwerte nach der Zeit sortiert und die Nummerierung angepasst."""

        self.data = self.data.sort_values("time").reset_index(drop= True)

        logging.info("Die CSV-Datei wurde sortiert.")

    def calculate_time_difference(self):
        """In der Methode wird wird die Zeitdifferenz zwischen den GPS-Daten in Sekunden berechnet."""

        self.data["delta_time"] = self.data["time"].diff.dt.total_seconds()
        self.data["delta_time"] = self.data["delta_time"].fillna(0)

        logging.info("Die Deltazeiten wurden berechnet.")

    
    def calculate_distance(self):
        """In dieser Methode wir die Wegdifferenz der GPS-Daten in Metern berechnet."""

        earth_radius = 6371000  # Erdradius in Metern

        lat = np.radians(self.data["lat"])
        lon = np.radians(self.data["lon"])

        delta_lat = lat.diff()
        delta_lon = lon.diff()

        a = (np.sin(delta_lat / 2) ** 2 + np.cos(lat.shift(1)) * np.cos(lat) * np.sin(delta_lon / 2) ** 2)

        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        self.data["distance"] = earth_radius * c
        self.data["distance"] = self.data["distance"].fillna(0)

        self.data["distance_total"] = self.data["distance"].cumsum()

        logging.info("Die Strecken zwischen den GPS-Punkten wurden berechnet.")
    
    def calculate_velocity(self):
        """In dieser Mehode wird die Momentangeschwindigkeit berechnet."""

        self.data["velocity"] = self.data["distance"] / self.data["delta_time"].replace(0, np.nan)

        self.data["velocity"] = self.data["velocity"].fillna(0)

        self.data["velocity_km/h"] = self.data["velocity"] * 3.6

        logging.info("Die Momentangeschwindigkeiten wurden berechnet.")
    
    def calculate_acceleration(self):
        """In der Methode wird die Beschleunigung berechnet."""

        self.data["acceleration"] = self.data["velocity"].diff() / self.data["delta_time"].replace(0, np.nan)

        self.data["acceleration"] = self.data["accelaration"].fillna(0)

        logging.info("Die Beschleunigungen wurden berechnet.")
    
    
    def calculate_gradient(self):
        """Diese Methode berechnet die Steigung zwischen zwei GPS Punkten."""

        self.data["elevation_difference"] = self.data["ele"].diff()

        self.data["gradient"] = self.data["elevation_difference"] / self.data["distance"].replace(0, np.nan)

        self.data["gradient"] = self.data["gradient"].fillna(0)

        self.data["gradient_percent"] = self.data["gradient"] * 100

        self.data["gradient_angle"] = np.arctan(self.data["gradient"])

        logging.info("Die Steigung wurde berechnet.")


    def calculate_drive_force(self):
        """In dieser Methode wird die Antriebskraft berechnet."""
        mass = 80.0          
        g  = 9.81            
        rho = 1.225          
        cw_a = 0.5625        


        self.data["air_force"] = 0.5 * rho * cw_a * self.data["velocity"] ** 2

        self.data["drive_force_raw"] = (mass * self.data["acceleration"]+ mass * g * np.sin(self.data["gradient_angle"])+ self.data["air_force"])

        self.data["drive_force"] = self.data["drive_force_raw"].clip(lower=0)

        logging.info("Antriebskraft wurde berechnet.")


    def calculate_drive_power(self):
        """In dieser Methode wird die Antriebsleistung berechnet."""
        self.data["drive_power"] = self.data["drive_force"] * self.data["velocity"]

        logging.info("Antriebsleistung wurde berechnet.")

    
    def calculate_torque(self):
        """In dieser Methode wird das Drehmoment berechnet."""
        wheel_radius = 34.29 

        self.data["torque"] = self.data["drive_force"] * wheel_radius

        logging.info("Drehmoment wurde berechnet.")


    def calculate_engine_current(self):
        """In dieser Methode wird der Motorstrom berechnet."""
        motor_constant = 1.5

        self.data["engine_current"] = self.data["torque"] / motor_constant

        logging.info("Motorstrom wurde berechnet.")


    
