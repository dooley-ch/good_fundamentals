# *******************************************************************************************
#  File:  __init__.py
#
#  Created: 27-05-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  27-05-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['find_folder', 'configure_logging', 'log_start', 'log_end', 'log_activity', 'find_data_folder']

from ._os import *
from ._logging import *
