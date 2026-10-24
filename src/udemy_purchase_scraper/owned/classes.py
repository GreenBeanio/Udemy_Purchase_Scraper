from dataclasses import dataclass
from decimal import Decimal
import datetime

@dataclass
class UdemyCoursePurchaseDetails:
    '''
    Stores purchase details for owned courses
    '''
    course_purchase: str
    course_date: datetime.date
    course_cost: Decimal

@dataclass
class UdemyCourseOwn:
    '''
    Store Udemy owned courses
    '''
    course_name: str
    course_link: str
    course_author: str
    course_page: str|None = None
    purchase: UdemyCoursePurchaseDetails|None = None

    def toExcelDict(self) -> dict[str, str | Decimal | datetime.datetime | None]:
        """
        x
        """
        return({
            "course_name": self.course_name,
            "course_author": self.course_author,
            "cost": self.purchase.course_cost if self.purchase is not None else Decimal(0),
            "purchase_date": self.purchase.course_date if self.purchase is not None else None, # No good way to have this be something other than None for the Excel output
            "purchase_number": self.purchase.course_purchase if self.purchase is not None else "Free"
        })