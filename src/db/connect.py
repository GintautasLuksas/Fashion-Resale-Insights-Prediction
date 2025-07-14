import os
import psycopg2
from psycopg2.extensions import connection as Psycopg2Connection, cursor as Psycopg2Cursor
from dotenv import load_dotenv
import logging
from typing import Optional, Type, Any

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

class DBEngine:
    """
    Manages connection and cursor for PostgreSQL database.

    Uses environment variables for configuration.
    """

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.connection: Optional[Psycopg2Connection] = None
        self.cursor: Optional[Psycopg2Cursor] = None
        self.logger = logger or logging.getLogger(__name__)
        self.connect()

    def connect(self) -> None:
        """Establishes DB connection using env variables."""
        try:
            self.connection = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
            )
            self.cursor = self.connection.cursor()
            self.logger.info('Database connection established.')
        except (Exception, psycopg2.Error) as error:
            self.logger.error(f'Error connecting to database: {error}')
            raise

    def __enter__(self) -> 'DBEngine':
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.logger.info('Database connection closed.')
