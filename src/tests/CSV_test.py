from ..simulation.GPS_data import CSVData

import matplotlib.pyplot as plt

GPS_test = CSVData("src/CSV_file/final_project_input_data.csv")

print(GPS_test.data.head(20))

print(GPS_test.data["engine_current"].max())

plt.figure(figsize=(10, 5))

plt.plot(GPS_test.data["time"], GPS_test.data["engine_current"])

plt.xlabel("Zeit")
plt.ylabel("Motorstrom in A")
plt.title("Motorstrom über der Zeit")
plt.grid(True)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()