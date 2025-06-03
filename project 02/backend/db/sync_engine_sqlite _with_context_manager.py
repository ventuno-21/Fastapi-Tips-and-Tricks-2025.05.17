import sqlite3
from typing import Any

from ..schemas.s_schemas import ShipmentCreate, ShipmentUpdate


class Database:

    def connect_to_db(self):
        self.connection = sqlite3.connect("shipmentDB.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS shipment
            (id INTEGER PRIMARY KEY , content TEXT, weight REAL, status TEXT)
            """
        )

    def create(self, shipment: ShipmentCreate):
        self.cursor.execute("SELECT MAX(id) FROM shipment")
        result = self.cursor.fetchone()
        new_id = (result[0] + 1) if result[0] is not None else 1
        self.cursor.execute(
            """INSERT INTO shipment  VALUES (:id ,:content,  :weight, :status)""",
            {"id": new_id, **shipment.model_dump(), "status": "placed"},
        )
        self.connection.commit()
        return new_id

    def get(self, id: int) -> dict[str, Any] | None:
        self.cursor.execute(
            f"SELECT id, content, weight FROM shipment WHERE id = {id} "
        )
        result = self.cursor.fetchone()

        if result is None:
            return None

        return {
            "result": result
            # "id": result[0],
            # "content": result[1],
            # "weight": result[2],
            # "status": result[3],
        }

    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any]:
        self.cursor.execute(
            """Update shipment SET status = :status WHERE id= :id""",
            {"id": id, **shipment.model_dump()},
        )
        self.connection.commit()
        return self.get(id)

    def delete(self, id: int):
        self.cursor.execute(f"DELETE From shipment WHERE id = {id}")
        self.connection.commit()

    def close(self):
        self.connection.close()

    def __enter__(self):
        print("enter a context")
        self.connect_to_db()
        self.create_table()
        return self

    def __exit__(self, *arg):
        print("exit a context")
        self.close()


def managed_db():
    db = Database()
    db.connect_to_db()
    db.create_table()

    yield db

    db.close()


with Database() as db:
    print(db.get(1))

# create a table


# # How to add data to out shipment table => You have to commit after insert a data to database
# cursor.execute("INSERT INTO shipment  VALUES (12071 ,'MY TEXT',  8.5, 'placed')")
# connection.commit()


# How to fetch a data from a table
# cursor.execute("SELECT id, content, weight FROM shipment ")
# result = cursor.fetchall()
# print(result)

# # Delete a data from database
# cursor.execute("DELETE From shipment WHERE id = 12071")
# connection.commit()


# Update
# cursor.execute("Update shipment SET status = 'in treansit' WHERE id=12071")
# connection.commit()


# # Update
# id=12071
# status='placed'
# cursor.execute(f"Update shipment SET status = '{status}' WHERE id={id}")
# connection.commit()


# # Drop a table
# cursor.execute("DROP TABLE shipment")
# connection.commit()


# connection.close()
