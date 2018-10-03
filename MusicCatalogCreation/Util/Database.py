""" Database operations
"""

import pyodbc
from pyodbc import Cursor, Connection, DatabaseError
from Util.AppSettings import AppSettings
from Exceptions import MException

class Database():
    """ manage database operations

    Attributes:
        connected:          True if already connected
        failed:
        cursor:             Database cursor
        nrecords:
        error_message:  Error Message
        config:             Configuration object (AppSettings)
        sql_connection:     database connection
    """

    def __init__(self, cfg) -> None:
        self.connected: bool = False
        self.failed: bool = False
        self.cursor: Cursor
        self.nrecords: int = 0
        self.processed: int = 0
        self.error_message: str = "OK"
        self.config: AppSettings = cfg
        self.sql_connection: Connection

    def ProcessException(self, sql: str, exc: Exception) -> str:
        """ Process database exception

            Args:
                sql:    SQL command that failed
                exc:    Exception thrown
            Raises:
            Returns:
                Error message (str)
        """
        self.failed = True
        # Build message
        message: str = ""
        if len(exc.args) > 1:
            message = exc.args[1] + " ||| " + sql
        else:
            message = "SQL Error " + sql
        self.error_message = message
        print(message)
        return message

    def Add(self, sql: str, *vals, commit=True, keep_connection: bool = False) -> bool:
        """ Insert a new record in the database

            Args:
                sql:    SQL command
                *vals:  values for the SQL command
                commit: True if commit after sql execution
            Raises:
            Returns:
                True if successful
        """
        if (not self.connected) and (self.failed or (not self.DBConnect())):
            self.error_message = "Invalid Connection"
            return False
        self.processed += 1
        try:
            self.nrecords = self.cursor.execute(sql, vals)
            if commit:
                self.cursor.commit()
            return True
        except DatabaseError as exc:
            self.ProcessException(sql, exc)
            return False
        finally:
            if not keep_connection:
                Connection.close(self.sql_connection)
                self.connected = False

    def Update(self, sql: str, *vals, commit=True, keep_connection: bool = False) -> bool:
        """ Execute a SQL Update

            Args:
                sql:    SQL command
                *vals:  values for the SQL command
                commit: True if commit after sql execution
            Raises:
            Returns:
                True if successful
        """
        if(not self.connected) and (self.failed or (not self.DBConnect())):
            self.error_message = "Invalid Connection"
            return False
        try:
            self.cursor.execute(sql, vals)
            if commit:
                self.cursor.commit()
            return True
        except DatabaseError as exc:
            self.ProcessException(sql, exc)
            return False
        finally:
            if not keep_connection:
                Connection.close(self.sql_connection)
                self.connected = False

    def Delete(self, sql: str, *vals, commit=True, keep_connection: bool = False) -> bool:
        """ Execute a SQL Delete

            Args:
                sql:    SQL command
                *vals:  values for the SQL command
                commit: True if commit after sql execution
            Raises:
            Returns:
                True if successful
        """
        if not self.connected and (self.failed or (not self.DBConnect())):
            self.error_message = "Invalid Connection"
            return False
        try:
            self.cursor.execute(sql, vals)
            if commit:
                self.cursor.commit()
            return True
        except DatabaseError as exc:
            self.ProcessException(sql, exc)
            return False
        finally:
            if not keep_connection:
                Connection.close(self.sql_connection)
                self.connected = False

    def Retrieve(self, sql: str, *vals, keep_connection: bool = False) -> bool:
        """ Execute a SQL SELECTArgs:

            Args:
                sql:    SQL command
                *vals:  values for the SQL command
            Raises:
            Returns:
                True if successful

        """
        if(not self.connected) and (self.failed or (not self.DBConnect())):
            self.error_message = "Invalid Connection"
            return False
        try:
            self.cursor.execute(sql, vals)
            return True
        except DatabaseError as exc:
            self.ProcessException(sql, exc)
            return False
        finally:
            if not keep_connection:
                Connection.close(self.sql_connection)
                self.connected = False

    def Execute(self, sql: str, keep_connection: bool = False) -> bool:
        """ Execute a SQL SP or command

            Args:
                sql:    SQL command
            Raises:
            Returns:
                True if successful
        """
        if (not self.connected) and (self.failed or (not self.DBConnect())):
            self.error_message = "Invalid Connection"
            return False
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
            return True

        except DatabaseError as dbexc:
            self.ProcessException(sql, dbexc)
            return False
        except MException as exc:
            self.ProcessException(sql, exc)
            return False
        finally:
            if not keep_connection:
                Connection.close(self.sql_connection)
                self.connected = False

    def DBConnect(self) -> bool:
        """ Connect to database

            Args:
            Raises:
            Returns:
                True if successful
        """
        try:
            self.sql_connection = pyodbc.connect('DSN=MusicSQL', autocommit=False)
            #self.sql_connection = pyodbc.connect('DSN=Music', autocommit=False)
            self.cursor = self.sql_connection.cursor()
            self.connected = True
            return True
        except DatabaseError as dbe:
            self.ProcessException("", dbe)
            return False
        except Exception as rxc:
            self.ProcessException("", rxc)
            return False

    def DBDisconnect(self) -> bool:
        """ Disconnect from database

            Args:
            Raises:
            Returns:
                True if successful
        """
        try:
            if self.sql_connection:
                Connection.close(self.sql_connection)
            return True
        except DatabaseError as dbe:
            self.ProcessException("", dbe)
            return False
