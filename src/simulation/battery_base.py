from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class BatteryBase(ABC):
    @abstractmethod
    def __init__(self, capacity_nom_Ah: float, initial_soc: float = 1.0):
        if not isinstance(capacity_nom_Ah, (int, float)):
            logger.error("Ungueltiger Datentyp fuer capacity_nom_Ah: %s", type(capacity_nom_Ah).__name__)
            raise TypeError("capacity_nom_Ah muss eine Zahl sein.")
        if capacity_nom_Ah <= 0:
            logger.error("Ungueltige Kapazitaet: %s", capacity_nom_Ah)
            raise ValueError("capacity_nom_Ah muss groesser als 0 sein.")
        if not isinstance(initial_soc, (int, float)):
            logger.error("Ungueltiger Datentyp fuer initial_soc: %s", type(initial_soc).__name__)
            raise TypeError("initial_soc muss eine Zahl sein.")

        self.C_nom = capacity_nom_Ah * 3600.0  # Kapazitaet in As
        self.soc = initial_soc
        if self.soc < 0:
            self.soc = 0.0
            logger.warning("Akku ist leer. SoC wurde auf 0 Prozent begrenzt.")
        elif self.soc > 1:
            self.soc = 1.0
            logger.warning("Akku ist voll. SoC wurde auf 100 Prozent begrenzt.")

        self.R_int = 0.08
        self.Vmin = 32.0
        self.Vmax = 42.0

    @abstractmethod
    def apply_current(self, current: float, duration: float) -> None:
        pass

    @abstractmethod
    def voltage(self, current: float = 0.0) -> float:
        pass
