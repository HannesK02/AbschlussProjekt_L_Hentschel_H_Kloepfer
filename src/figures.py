import matplotlib.pyplot as plt


from simulation.GPS_data import CSVData

gps_data = CSVData("src/CSV_file/final_project_input_data.csv")






class FigureCreator:
    def __init__(self, data):
        self.data = data

    def engine_current(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(self.data["time"], self.data["engine_current"])
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Motorstrom in A")
        ax.set_title("Motorstrom über der Zeit")
        ax.grid(True)

        fig.autofmt_xdate()
        fig.tight_layout()

        return fig

    def battery_soc(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(self.data["time"], self.data["battery_soc_percent"])
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Akkustand in %")
        ax.set_title("Akkustand über der Zeit")
        ax.grid(True)

        fig.autofmt_xdate()
        fig.tight_layout()

        return fig

    def battery_voltage(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(self.data["time"], self.data["battery_voltage"])
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Spannung in V")
        ax.set_title("Akkuspannung über der Zeit")
        ax.grid(True)

        fig.autofmt_xdate()
        fig.tight_layout()

        return fig