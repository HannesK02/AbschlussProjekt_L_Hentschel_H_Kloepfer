from src.simulation.GPS_data import CSVData
from src.simulation.battery_pack import (
    BatteryPack,
    LiPo_SoC,
    LiPo_UoC,
    NMC_SoC,
    NMC_UoC,
)
from src.simulation.battery_simulation import BatterySimulation


cell_capacity_Ah = 3.0
cells_series = 10
cells_parallel = 4

capacity_nom_Ah = cell_capacity_Ah * cells_parallel

lipo_resistance_mOhm = cells_series * 8.0 / cells_parallel
nmc_resistance_mOhm = cells_series * 7.0 / cells_parallel

gps_data = CSVData("src/CSV_file/final_project_input_data.csv")

lipo_akku = BatteryPack(
    capacity_nom_Ah=capacity_nom_Ah,
    internal_resistance_mOhm=lipo_resistance_mOhm,
    initial_soc=1.0,
    Vmin=32.0,
    Vmax=42.0,
    soc_points=LiPo_SoC,
    ocv_points=LiPo_UoC,
)

nmc_akku = BatteryPack(
    capacity_nom_Ah=capacity_nom_Ah,
    internal_resistance_mOhm=nmc_resistance_mOhm,
    initial_soc=1.0,
    Vmin=32.0,
    Vmax=42.0,
    soc_points=NMC_SoC,
    ocv_points=NMC_UoC,
)

lipo_results = BatterySimulation(gps_data, lipo_akku).run()
nmc_results = BatterySimulation(gps_data, nmc_akku).run()

print("LiPo Akku nach der Strecke:")
print(lipo_akku)
print("Erste Werte:")
print(lipo_results[["time", "engine_current", "battery_soc_percent", "battery_voltage"]].head().to_string())
print("Letzte Werte:")
print(lipo_results[["time", "engine_current", "battery_soc_percent", "battery_voltage"]].tail().to_string())

print("\nNMC Akku nach der Strecke:")
print(nmc_akku)
print("Erste Werte:")
print(nmc_results[["time", "engine_current", "battery_soc_percent", "battery_voltage"]].head().to_string())
print("Letzte Werte:")
print(nmc_results[["time", "engine_current", "battery_soc_percent", "battery_voltage"]].tail().to_string())
