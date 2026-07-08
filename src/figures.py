import matplotlib.pyplot as plt


class FigureCreator:
    def __init__(self, data):
        self.data = data

    def velocity(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(self.data["time"], self.data["velocity_km/h"])
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Geschwindigkeit in km/h")
        ax.set_title("Geschwindigkeit")
        ax.grid(True)

        fig.autofmt_xdate()
        fig.tight_layout()

        return fig

    def drive_power(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(self.data["time"], self.data["drive_power"])
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Leistung in W")
        ax.set_title("Leistung")
        ax.grid(True)

        fig.autofmt_xdate()
        fig.tight_layout()

        return fig

    def battery_soc(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(self.data["time"], self.data["battery_soc_percent"])
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Akkustand in %")
        ax.set_title("Akkustand ueber der Zeit")
        ax.grid(True)

        fig.autofmt_xdate()
        fig.tight_layout()

        return fig

    def elevation_profile(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(self.data["distance_total"] / 1000, self.data["ele"])
        ax.set_xlabel("Strecke in km")
        ax.set_ylabel("Hoehe in m")
        ax.set_title("Hoehenprofil der Fahrt")
        ax.grid(True)

        fig.tight_layout()

        return fig

    def engine_current(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(self.data["time"], self.data["engine_current"])
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Motorstrom in A")
        ax.set_title("Motorstrom")
        ax.grid(True)

        fig.autofmt_xdate()
        fig.tight_layout()

        return fig

    def battery_voltage(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(self.data["time"], self.data["battery_voltage"])
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Spannung in V")
        ax.set_title("Akkuspannung")
        ax.grid(True)

        fig.autofmt_xdate()
        fig.tight_layout()

        return fig
