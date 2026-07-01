import logging

from battery_base import BatteryBase

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

        open_circuit_voltage = self.Vmin + self.soc * (self.Vmax - self.Vmin)
        return open_circuit_voltage - self.R_int * current

    def is_empty(self) -> bool:
        return self.soc <= 0.0 + 1e-9

    def is_full(self) -> bool:
        return self.soc >= 1.0 - 1e-9

    def __str__(self):
        return f"BatteryPack(SoC={self.soc * 100:.1f}%, V={self.voltage():.2f} V)"
