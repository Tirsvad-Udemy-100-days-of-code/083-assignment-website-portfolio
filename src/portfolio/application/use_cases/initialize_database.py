"""!
@file initialize_database.py
@brief Use case: create the storage of the portfolio, or confirm that it is ready.
"""

from portfolio.application.ports.database_initializer import DatabaseInitializer


def initialize_database(initializer: DatabaseInitializer) -> bool:
    """!
    @brief Prepare the storage for the current version of the program.
    @param initializer Creates the storage.
    @return True when the storage was created, False when it was already ready.
    @throws SchemaVersionError The storage was made by a newer program.
    @throws DataSourceError The storage cannot be used.
    """
    return initializer.initialize()
