import logging

from .battery_base import BatteryBase

logger = logging.getLogger(__name__)


def _validate_number(name: str, value: float) -> None:
    if not isinstance(value, (int, float)):
        logger.error("Ungueltiger Datentyp fuer %s: %s", name, type(value).__name__)
        raise TypeError(f"{name} muss eine Zahl sein.")


def _validate_positive_number(name: str, value: float) -> None:
    _validate_number(name, value)
    if value <= 0:
        logger.error("Ungueltiger Zahlenwert fuer %s: %s", name, value)
        raise ValueError(f"{name} muss groesser als 0 sein.")


class BatteryPack(BatteryBase):
    def __init__(
        self,
        capacity_nom_Ah: float,
        internal_resistance_mOhm: float = 80.0,
        initial_soc: float = 1.0,
        Vmin: float = 3.0,
        Vmax: float = 4.2,
        soc_points: list[float] | None = None,
        ocv_points: list[float] | None = None,
    ):
        _validate_positive_number("capacity_nom_Ah", capacity_nom_Ah)
        _validate_number("internal_resistance_mOhm", internal_resistance_mOhm)
        if internal_resistance_mOhm < 0:
            logger.error("Ungueltiger Innenwiderstand: %s", internal_resistance_mOhm)
            raise ValueError("internal_resistance_mOhm darf nicht negativ sein.")
        _validate_number("initial_soc", initial_soc)
        _validate_positive_number("Vmin", Vmin)
        _validate_positive_number("Vmax", Vmax)
        if Vmax <= Vmin:
            logger.error("Ungueltiger Spannungsbereich: Vmin=%s, Vmax=%s", Vmin, Vmax)
            raise ValueError("Vmax muss groesser als Vmin sein.")

        self.C_nom = capacity_nom_Ah * (60.0 * 60.0)
        self.soc = initial_soc
        self._limit_soc()
        self.R_int = internal_resistance_mOhm * 1e-3

        self.Vmin = Vmin
        self.Vmax = Vmax
        self.soc_points = soc_points
        self.ocv_points = ocv_points
        self._validate_ocv_curve()

    def _validate_ocv_curve(self) -> None:
        if self.soc_points is None and self.ocv_points is None:
            return
        if self.soc_points is None or self.ocv_points is None:
            raise ValueError("soc_points und ocv_points muessen gemeinsam angegeben werden.")
        if len(self.soc_points) != len(self.ocv_points):
            raise ValueError("soc_points und ocv_points muessen gleich lang sein.")
        if len(self.soc_points) < 2:
            raise ValueError("Die Kennlinie benoetigt mindestens zwei Punkte.")

        for soc in self.soc_points:
            _validate_number("SoC-Kennlinienwert", soc)
            if not 0.0 <= soc <= 1.0:
                raise ValueError("Alle SoC-Kennlinienwerte muessen zwischen 0 und 1 liegen.")
        for voltage in self.ocv_points:
            _validate_positive_number("OCV-Kennlinienwert", voltage)

        if self.soc_points[0] != 0.0 or self.soc_points[-1] != 1.0:
            raise ValueError("Die SoC-Kennlinie muss bei 0 beginnen und bei 1 enden.")
        if any(left >= right for left, right in zip(self.soc_points, self.soc_points[1:])):
            raise ValueError("Die SoC-Kennlinienwerte muessen streng aufsteigend sein.")

    def _limit_soc(self) -> None:
        if self.soc < 0:
            self.soc = 0.0
            logger.warning("Akku ist leer. SoC wurde auf 0 Prozent begrenzt.")
        elif self.soc > 1:
            self.soc = 1.0
            logger.warning("Akku ist voll. SoC wurde auf 100 Prozent begrenzt.")

    def apply_current(self, current: float, duration: float) -> None:
        _validate_number("current", current)
        _validate_positive_number("duration", duration)

        dsoc = -(current * duration) / self.C_nom
        self.soc += dsoc
        self._limit_soc()

    def voltage(self, current: float = 0.0) -> float:
        _validate_number("current", current)

        open_circuit_voltage = self._open_circuit_voltage()
        return open_circuit_voltage - self.R_int * current

    def _open_circuit_voltage(self) -> float:
        if self.soc_points is None or self.ocv_points is None:
            return self.Vmin + self.soc * (self.Vmax - self.Vmin)

        for index in range(len(self.soc_points) - 1):
            soc_low = self.soc_points[index]
            soc_high = self.soc_points[index + 1]

            if soc_low <= self.soc <= soc_high:
                voltage_low = self.ocv_points[index]
                voltage_high = self.ocv_points[index + 1]
                factor = (self.soc - soc_low) / (soc_high - soc_low)
                return voltage_low + factor * (voltage_high - voltage_low)
            
        return self.ocv_points[-1]

    def is_empty(self) -> bool:
        return self.soc <= 0.0 + 1e-9

    def is_full(self) -> bool:
        return self.soc >= 1.0 - 1e-9

    def __str__(self):
        return f"BatteryPack(SoC={self.soc * 100:.1f}%, V={self.voltage():.2f} V)"


LiPo_SoC = [0.00, 0.04, 0.09, 0.13, 0.17, 0.21, 0.26, 0.30, 0.40, 0.52, 0.64, 0.76, 0.88, 1.00]
LiPo_UoC = [32.00, 35.87, 36.85, 37.56, 37.87, 38.28, 38.81, 39.05, 39.55, 40.27, 40.70, 41.16, 41.65, 42.00]

NMC_SoC = [0.00, 0.04, 0.09, 0.13, 0.17, 0.21, 0.26, 0.30, 0.40, 0.52, 0.64, 0.76, 0.88, 1.00]
NMC_UoC = [32.00, 32.61, 33.17, 33.85, 34.24, 34.66, 35.38, 35.65, 36.65, 37.64, 38.91, 40.14, 41.08, 42.00]

cell_capacity_Ah = 3.0
cells_series = 10
cells_parallel = 4

capacity_nom_Ah = cell_capacity_Ah * cells_parallel

lipo_resistance_mOhm = cells_series * 8.0 / cells_parallel
nmc_resistance_mOhm = cells_series * 7.0 / cells_parallel

LiPo_Akku = BatteryPack(
    capacity_nom_Ah=capacity_nom_Ah,
    internal_resistance_mOhm=lipo_resistance_mOhm,
    initial_soc=1.0,
    Vmin=32.0,
    Vmax=42.0,
    soc_points=LiPo_SoC,
    ocv_points=LiPo_UoC,
    )

NMC_Akku = BatteryPack(
    capacity_nom_Ah=capacity_nom_Ah,
    internal_resistance_mOhm=nmc_resistance_mOhm,
    initial_soc=1.0,
    Vmin=32.0,
    Vmax=42.0,
    soc_points=NMC_SoC,
    ocv_points=NMC_UoC,
)