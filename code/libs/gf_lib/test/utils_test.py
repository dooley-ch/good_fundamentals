# *******************************************************************************************
#  File:  utils_test.py
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

from pathlib import Path
import gf_lib.utils as utils


def test_find_folder__is_current_folder() -> None:
    current_folder = Path("../../../apps/logs").resolve()
    folder: Path = utils.find_folder('logs', current_folder)
    assert current_folder == folder


def test_find_folder__one_folder_up() -> None:
    current_folder = Path("../../../apps").resolve()
    folder: Path = utils.find_folder('logs', current_folder)
    assert current_folder.joinpath('logs') == folder


def test_find_folder__one_folder_further_up() -> None:
    current_folder = Path("/Volumes/LaCie/Dev/Good_Fundamentals").resolve()
    folder: Path = utils.find_folder('logs', current_folder)
    assert folder is None
