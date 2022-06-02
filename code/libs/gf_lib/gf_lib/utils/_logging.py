# *******************************************************************************************
#  File:  config_utils.py
#
#  Created: 23-05-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  23-05-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['configure_logging', 'log_start', 'log_end', 'log_activity']

from pathlib import Path
from loguru import logger
from ._os import find_logs_folder


class ActivityFileFormatter:
    def __init__(self):
        self._default_format = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {function: ^15} | {file: ^15} | {line: >3} " \
                               "" \
                               "| {message} \n"
        self._line_format = "========================================== {time:YYYY-MM-DD HH:mm:ss} " \
                            "=============================================== \n"

    def format(self, record):
        if 'line' in record["extra"]:
            return self._line_format

        return self._default_format


def configure_logging(root_name: str, root_folder: Path | str | None = None):
    file_format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {function: ^15} | {file: ^15} | {line: >3} | {" \
                       "message}"

    logs_folder = find_logs_folder(root_folder)
    core_file = logs_folder.joinpath(f"core_{root_name}.log")
    errors_file = logs_folder.joinpath(f"errors_{root_name}.log")
    activity_file = logs_folder.joinpath(f"activity_{root_name}.log")

    activity_formatter = ActivityFileFormatter()

    logger.remove()

    logger.level("LINE", no=60, color="<white>")

    logger.add(core_file, rotation='1 day', retention='5 days', compression='zip', level='INFO',
               backtrace=True, diagnose=True, format=file_format)
    logger.add(errors_file, rotation='1 day', retention='5 days', compression='zip', level='ERROR',
               backtrace=True, diagnose=True, format=file_format)
    logger.add(activity_file, rotation='1 day', retention='5 days', compression='zip', level='SUCCESS',
               filter=lambda record: "activity" in record["extra"], format=activity_formatter.format)


def log_start():
    logger.bind(activity=True, line=True).log("LINE", 'Start')


def log_end():
    logger.bind(activity=True, line=True).log("LINE", 'End')


def log_activity(message: str) -> None:
    logger.bind(activity=True).success(message)
