# *******************************************************************************************
#  File:  errors.py
#
#  Created: 30-05-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  30-05-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['ApplicationError', 'DuplicateRecordError', 'RequestFailedError', 'RequestMaxFailedError',
           'RequestResponseError', 'ApiFailedError']


class ApplicationError(Exception):
    pass


class DatastoreError(ApplicationError):
    pass


class DuplicateRecordError(DatastoreError):
    def __init__(self, key: str):
        super().__init__(f"A record with the key: {key}, already exists in the collection")


class HttpError(ApplicationError):
    pass


class RequestFailedError(HttpError):
    def __init__(self, url: str, status_code: int):
        super().__init__(f"Failed to download url: {url}, status: {status_code}")


class RequestMaxFailedError(HttpError):
    def __init__(self, url: str, status_code: int):
        super().__init__(f"Max requests exceeded: {url}, status: {status_code}")


class RequestResponseError(HttpError):
    pass


class ApiFailedError(HttpError):
    pass
