"""!
@file database_initializer.py
@brief Port through which the use cases prepare the storage.
"""

from typing import Protocol


class DatabaseInitializer(Protocol):
    """!
    @brief Creates the storage of the portfolio, or confirms that it is ready.
    """

    def initialize(self) -> bool:
        """!
        @brief Create the storage when it is missing.
        @return True when the storage was created, False when it was already
            ready for this version of the program.
        @throws SchemaVersionError The storage was made by a newer program.
        """
        ...
