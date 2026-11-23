import sqlite3
import os
from enum import Enum
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
databaseName = BASE_DIR / "database.db"

class statusCode(Enum):
    SUCCESS=0
    FAIL=1
    EXIST=2
    NOT_EXIST=3

# databaseName = "./database/database.db"

def parseStr(s: str) -> str:
    if not isinstance(s, str): raise TypeError("musi być typ str")
    s = s.strip()
    if not s: raise TypeError("str nie mogą być tylko spacje")
    return s

# aby utworzyć baze na testy
def conectTo(name:str):
    global databaseName
    databaseName = BASE_DIR/name

def reset() -> None:
    if os.path.exists(databaseName):
        os.remove(databaseName)
    
    conn = sqlite3.connect(databaseName)

    with open(BASE_DIR / "db_init.sql") as f:
        conn.executescript(f.read())
    
    conn.commit()
    conn.close()

def remove() -> None:
    if os.path.exists(databaseName):
        os.remove(databaseName)

def printTalble(name:str, cursor:sqlite3.Cursor):
    cursor.execute(f"SELECT * FROM {name}")
    rows = cursor.fetchall()
    print(name)
    for row in rows:
        print(row)

def printAll():
    conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()

    printTalble("user",cursor)
    printTalble("team",cursor)
    printTalble("team_user",cursor)

    conn.commit()
    conn.close()

def create(table:str, colm:list, val:list):
    conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()

    retCode = statusCode.SUCCESS
    newId = 0
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        query = f"INSERT INTO {table} ({','.join(colm)}) VALUES ({','.join(["?"]*len(colm))})"
        cursor.execute(query, val)
        newId = cursor.lastrowid
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if e.sqlite_errorname == "SQLITE_CONSTRAINT_UNIQUE": retCode = statusCode.EXIST
        elif e.sqlite_errorname == "SQLITE_CONSTRAINT_FOREIGNKEY": retCode = statusCode.NOT_EXIST
        else: raise
    finally:
        conn.close()

    return newId, retCode

def update(table:str, id:int, colm:list, val:list)->statusCode:
    if len(colm) != len(val):
        raise ValueError("colm i val nie maja takiej samej długości")
    
    conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()

    query = f"UPDATE {table} SET {','.join(colm)} WHERE id=?"
    val.append(id)
    retCode = statusCode.SUCCESS
    try:
        cursor.execute(query, val)
        if cursor.rowcount == 0:
            retCode = statusCode.NOT_EXIST
        elif cursor.rowcount > 1:
            raise Exception("były duplikaty, jakoś")
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if not e.sqlite_errorname == "SQLITE_CONSTRAINT_UNIQUE": raise
        retCode = statusCode.EXIST
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()

    return retCode

def read(table:str, ids:list[int] | None, colm:list[str]) -> list:
    find = []
    values = []

    if ids is not None:
        for i in ids:
            find.append("?")
            values.append(i)

    conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()

    query = f"SELECT id, {','.join(colm)} FROM {table}"
    if ids is not None:
        query += f" WHERE id in ({','.join(find)})" # id jak narazie zostaje dla table

    cursor.execute(query, values)
    data = cursor.fetchall()

    conn.close()

    return data

def readId(table:str, where:str, val:list) -> list[int]:
    conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()

    query = f"SELECT id FROM {table} WHERE " + where

    cursor.execute(query, val)
    data = cursor.fetchall()
    data = [i[0] for i in data]

    conn.close()

    return data

def delete(table:str, id:int):
    # triger handels usuwanie
    conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()

    retCode = statusCode.SUCCESS
    try:
        cursor.execute(
            f"DELETE FROM {table} WHERE id=?",
            (id,)
        )

        if cursor.rowcount == 0:
            retCode = statusCode.NOT_EXIST
        elif cursor.rowcount > 1:
            raise Exception("były duplikaty, jakoś")

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

    conn.close()

    return retCode

if __name__ == "__main__":
    printAll()
    reset()