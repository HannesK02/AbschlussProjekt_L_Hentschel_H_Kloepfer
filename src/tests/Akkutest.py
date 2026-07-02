from src.simulation.battery_pack import BatteryPack, LiPo_SoC, LiPo_UoC, NMC_SoC, NMC_UoC

cell_capacity_Ah = 3.0
cells_series = 10
cells_parallel = 4

capacity_nom_Ah = cell_capacity_Ah * cells_parallel

lipo_resistance_mOhm = cells_series * 8.0 / cells_parallel
nmc_resistance_mOhm = cells_series * 7.0 / cells_parallel

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

print(lipo_akku)
print(nmc_akku)

lipo_akku.apply_current(current=10.0, duration=60.0)

print(lipo_akku)
print(lipo_akku.voltage(current=10.0))