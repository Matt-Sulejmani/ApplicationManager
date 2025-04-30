# Std lib imports
import logging
from pathlib import Path
import json
from typing import Dict, Any
from dataclasses import dataclass, field
import datetime
import sqlite3
import argparse


# Global values
logger: logging.Logger = logging.getLogger(__name__)
config_path: str | Path = Path("config.json")

# Load configs into memory
with open(config_path, "r") as file:
    configs: Dict[str, Any] = json.load(file)

# For degugging purposes
logger.setLevel(logging.DEBUG)


# TODO
# 1. Add deadlines from files
# 2. Add deadlines from CLI
# 3. Make a GUI to display data
# 4. Write tests




@dataclass(slots=True, eq=True)
class Application:
    name: str
    class_id: int
    due_date: datetime.date = field(default_factory=datetime.date)
    due_time: datetime.time = field(default_factory=datetime.time)
    
    #* Finished - Testing
    def is_unique(self, connection: sqlite3.Connection) -> bool:
        """Check if the current object is unique or if there is already an entry in the 
        database with the same data. If no entry is found the function returns False.

        Args:
            connection (sqlite3.Connection): Required sql connection object that connects
            to the desired database.

        Returns:
            bool: Returns wether another entry with the same data as the current 
            object already exists in the database
        """
        c = connection.cursor()

        c.execute("SELECT * FROM deadlines WHERE (deadline = :deadline AND time = :time AND class_id = :class_id AND name = :name)",
                  {"deadline": str(self.due_date), "time": str(self.due_time), "class_id": self.class_id, "name": self.name})
        
        if len(c.fetchall()) == 0:
            return True
        
        return False

    #* Finished - Testing
    def add_to_database(self, connection: sqlite3.Connection) -> None:
        """Add the current application deadline to the database file if it is not already
        in the database. In case another application has the same data, the function raises an error.

        Args:
            connection (sqlite3.Connection): Enter the database connection object

        Raises:
            Exception: If something goes wrong when trying to execute the sql command this
            function will raise an exception.
        """
        try:
            c = connection.cursor()

            # Do not add deadline if it is already in the database
            if (not self.is_unique(connection)):
                raise Exception("Deadline is already in the database")
            
            # Add deadline if it is not in database
            c.execute("INSERT INTO deadlines VALUES (:deadline, :time, :name, :class_id)",
                      {"deadline": str(self.due_date), "time": str(self.due_time), "name": self.name, "class_id":self.class_id})
        
            
            connection.commit()

        except Exception as e:
            logger.warning("Something went wrong when trying to insert deadline into database!")
            raise e
    
    def edit_deadline(self) -> None:


        return NotImplementedError


    def delete_from_database(self, connection: sqlite3.Connection) -> None:


        return NotImplementedError

#* Finished
def table_setup(connection: sqlite3.Connection) -> None:
    """Creates the table within the data.db file. This function should only run
    if the table has not been created!

    Args:
        connection (sqlite3.Connection): Enter the database connection object

    Raises:
        Exception: If something goes wrong when trying to execute the sql command this
        function will raise an exception.
    """
    try:
        c = connection.cursor()

        # Create the table when the program is first run
        c.execute("""CREATE TABLE deadlines (
                    deadline text,
                    time text,
                    name text,
                    class_id integer)""")
    
        connection.commit()

        # Show in the config.json file that the table has been created
        with open(config_path, "w") as file:
            configs['_TABLE_EXISTS'] = True
            json.dump(configs, file, indent=4)

        logger.info("Created database successfully.")

    except sqlite3.OperationalError as e:
        logger.warning("Something went wrong with the SQL command")
        raise e

#* FInished
def create_database(connection: sqlite3.Connection) -> None:
    """Used to check if table already exists, if not it calls the 
    table_setup function, otherwise it logs to the console that the 
    table already exists in the database.

    Args:
        connection (sqlite3.Connection): _description_
    """
    if (not configs["_TABLE_EXISTS"]):
        table_setup(connection)

    else:
        logger.info("Table is already created within the database file.")


def show_in_database(connection: sqlite3.Connection) -> None:
    c = connection.cursor()

    c.execute("SELECT * FROM deadlines")
    print(c.fetchall())



def main():
    conn = sqlite3.connect('data.db')

    create_database(conn)

    app = Application("test", 1, datetime.date.fromisoformat('20250430'), datetime.time(18))
    # app.add_to_database(conn)

    show_in_database(conn)
    

    conn.close()
    



if __name__ == "__main__":
    main()
