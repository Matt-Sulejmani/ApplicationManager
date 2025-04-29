# Std lib imports
from dataclasses import dataclass, field
import datetime
import sqlite3
import logging
import argparse

# Dependencies
import customtkinter as ctk


# Global values

logger = logging.getLogger(__name__)


# For degugging purposes
logger.setLevel(logging.DEBUG)



class MainWin(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("600x500")




@dataclass(slots=True, eq=True)
class Application:
    name: str
    class_id: int
    due_date: datetime.date = field(default_factory=datetime.date)
    due_time: datetime.time = field(default_factory=datetime.time)
    

    def is_unique(self, connection: sqlite3.Connection) -> bool:
        # Not finished
        c = connection.cursor()

        c.execute("SELECT * FROM deadlines WHERE conditions")


    def add_to_database(self, connection: sqlite3.Connection) -> None:
        
        try:
            c = connection.cursor()

            if (not self.is_unique()):
                raise Exception("Deadline is already in the database")
            
            

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
    

def create_database(connection: sqlite3.Connection) -> None:
    try:
        c = connection.cursor()

        # Create the table when the program is first run
        c.execute("""CREATE TABLE deadlines (
                    deadline text,
                    time text,
                    name text,
                    class_id integer)""")
    
        connection.commit()

        logger.info("Created database successfully.")

    except sqlite3.OperationalError as e:
        logger.warning("Something went wrong with the SQL command")
        raise e


def show_in_database(connection: sqlite3.Connection) -> None:
    c = connection.cursor()

    c.execute("SELECT * FROM deadlines")
    print(c.fetchall())



def main():
    conn = sqlite3.connect('data.db')


    # Check if database already esists
    # Create the database if it doesn't
    # create_database(conn)

    app = Application("test", 1, datetime.date.fromisoformat('20250430'), datetime.time(18))
    app.add_to_database(conn)

    show_in_database(conn)
    

    conn.close()
    



if __name__ == "__main__":
    main()
