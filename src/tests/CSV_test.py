from ..simulation.GPS_data import CSVData

import matplotlib.pyplot as plt

GPS_test = CSVData("src/CSV_file/final_project_input_data.csv")

print(GPS_test.data.head(20))
