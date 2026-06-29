import pandas as pd
import logging

class CSVData:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = pd.read_csv(csv_file)

        logging.info("CSV-Datei wurde eingelesen.")

        self.validate()
        self.prepare()
        self.sort_by_time()
        


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
        self.data = self.data.sort_values("time").reset_index(drop= True)

        logging.info("Die CSV-Datei wurde sortiert.")
