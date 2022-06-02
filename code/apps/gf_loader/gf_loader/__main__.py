# *******************************************************************************************
#  File:  __main__.py
#
#  Created: 01-06-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  01-06-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

from gf_lib.utils import configure_logging, log_start, log_end


def main() -> None:
    configure_logging('gf_loader', __file__)
    log_start()

    print('Hello, world')

    log_end()


if __name__ == '__main__':
    main()
