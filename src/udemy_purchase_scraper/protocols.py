from typing import Protocol

class ExcelOutputable(Protocol):
    """
    Class that can be turned into a dictionary for a Pandas Data Frame
    """
    def toExcelDict() -> dict[str, any]:
        """
        Turns a class into a dictionary for a Pandas Data Frame
        """
        ...