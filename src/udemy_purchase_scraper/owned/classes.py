from dataclasses import dataclass
from decimal import Decimal
import datetime

@dataclass
class UdemyCoursePurchaseDetails:
    course_purchase: str
    course_date: datetime.date
    course_cost: Decimal

@dataclass
class UdemyCourseOwn:
    '''
    A class to store Udemy courses
    '''
    course_name: str
    course_link: str
    course_author: str
    course_page: str|None = None
    purchase: UdemyCoursePurchaseDetails|None = None