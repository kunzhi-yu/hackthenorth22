import json
import bitdotio

with open("key") as f:
    key = f.readline()
b = bitdotio.bitdotio(key)

# Create table, if it does not already exist
create_table_sql = """
    CREATE TABLE TASKS (
      id text,
      title text,
      description text,
      deadline text
    )
    """

with b.get_connection("DeathByThermodynamics/hackthenorth2022") as conn:
    cursor = conn.cursor()
    try:
        cursor.execute(create_table_sql)
    except:
        pass

def get_data_by_id(userid):
    """use this for backend
    """
    sql = f"SELECT * FROM TASKS WHERE id = '{userid}';"
    while True:
        try:
            cursor.execute(sql)
            break
        except:
            pass
    return [{"id": i[0], "title": i[1], "description": i[2], "deadline": i[3]} for i in cursor.fetchall()]


def get_all_db():
    """Return a json of the db
    """
    sql = f"SELECT * FROM TASKS ORDER BY id;"
    while True:
        try:
            cursor.execute(sql)
            break
        except:
            pass
    return [{"id": i[0], "title": i[1], "description": i[2],"deadline": i[3]} for i in cursor.fetchall()]


def write(input_dict):
    """Set a new observation to the db
    """
    sql = """INSERT INTO TASKS (id, title, description, deadline)
             VALUES(%s, %s, %s, %s);"""
    records = list(input_dict.values())
    while True:
        try:
            cursor.execute(sql, records)
            break
        except:
            pass

def query_entry(title: str):
    sql = f"SELECT * FROM TASKS WHERE title = '{title}';"
    while True:
        try:
            cursor.execute(sql)
            conn.commit()
            break
        except:
            pass
    c = cursor.fetchone()
    return {
        "id": c[0],
        "title": c[1],
        "description": c[2],
        "deadline": c[3]
    }

def delete_entry(title):
    """Remove an entry from the database.
    """
    sql = f"DELETE FROM TASKS WHERE title = '{title}';"
    while True:
        try:
            cursor.execute(sql)
            conn.commit()
            break
        except:
            pass
