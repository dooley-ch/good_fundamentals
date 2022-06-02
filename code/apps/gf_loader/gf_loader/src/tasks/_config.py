# *******************************************************************************************
#  File:  _config.py
#
#  Created: 02-06-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  02-06-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['ConfigDatabase']

import luigi


class ConfigDatabase(luigi.Config):
    """
    This class provides access to the database params stored in the luigi config file
    """
    url: str = luigi.Parameter()
    database: str = luigi.Parameter()
