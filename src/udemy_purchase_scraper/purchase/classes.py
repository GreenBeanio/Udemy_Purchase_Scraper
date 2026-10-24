from dataclasses import dataclass
from decimal import Decimal
import datetime

@dataclass
class UdemyCoursePurchase:
    '''
    Stores Udemy courses for purchases
    '''
    course_name: str
    course_link: str
    course_cost: Decimal

@dataclass
class UdemyPurchase:
    '''
    Stores Udemy purchases
    '''
    purchase_number: str
    purchase_date: datetime.date
    purchase_cost: Decimal
    courses: any|None = None

    def toExcelDict(self) -> dict[str, str, datetime.datetime, Decimal]:
        """
        x
        """
        return({
            "purchase_number": self.purchase_number,
            "purchase_date": self.purchase_date,
            "purchase_cost": self.purchase_cost
        })