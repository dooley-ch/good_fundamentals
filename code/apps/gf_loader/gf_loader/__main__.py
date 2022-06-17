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

from pathlib import Path
import atexit
import os
import luigi
import typer
from gf_lib.utils import configure_logging, log_start, log_end, log_activity
import src.tasks as tasks

app = typer.Typer(help='This application handles the ETL process needed to build the gf database')


@app.command('populate', help='Populate the database with a new master list')
def populate():
    log_activity('Populating master list...')

    if luigi.build([tasks.PopulateDatabaseTask()], local_scheduler=True):
        typer.echo('Database populated.', color=True)
        log_activity('Database populated successfully.')
    else:
        typer.echo('Failed to populate database, see log files for details.', err=True, color=True)
        log_activity('Failed to populate database.')


@app.command('reset', help='Deletes expired company records')
def reset():
    log_activity('Resetting system...')

    if luigi.build([tasks.ResetTask()], local_scheduler=False):
        typer.echo('System has been reset.', color=True)
        log_activity('System reset completed successfully.')
    else:
        typer.echo('System reset failed, see log files for details.', err=True, color=True)
        log_activity('System reset failed.')


def exit_routine() -> None:
    log_end()


def main() -> None:
    # Set the working folder
    working_folder: Path = Path(__file__).parent
    os.chdir(working_folder)

    # Set up the exit routine
    atexit.register(exit_routine)

    # Configure logging
    configure_logging('gf_loader', __file__)
    log_start()

    # Process commands
    app()


if __name__ == '__main__':
    main()
