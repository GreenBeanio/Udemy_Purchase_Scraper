class RetryError(Exception):
    '''Raised when there are no more retries'''

class SingleCourseError(Exception):
    '''Raised when a purchase only has a single course'''

class LastPageError(Exception):
    '''Raised when there are no more purchase pages'''