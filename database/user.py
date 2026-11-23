from . import _admin
from ._admin import statusCode
import sqlite3

def create(login:str, password:str) -> tuple[int, statusCode]:
    login = _admin.parseStr(login)
    password = _admin.parseStr(password)

    return _admin.create(
        "user", 
        ["login", "password", "name"],
        [login,password,login]
    )

def read(ids:list[int]|None=None, login:bool=True, name:bool=True) -> list:
    colm=[]
    if(login): colm.append("login")
    if(name): colm.append("name")
    return _admin.read("user", ids, colm)

def delete(id:int) -> statusCode:
    return _admin.delete("user", id)

def update(id:int, newLogin:str=None, newPassword:str=None, newName:str=None) -> statusCode:
    updates = []
    values = []

    if newLogin is not None:
        updates.append("login = ?")
        values.append(_admin.parseStr(newLogin))

    if newPassword is not None:
        updates.append("password = ?")
        values.append(_admin.parseStr(newPassword))

    if newName is not None:
        updates.append("name = ?")
        values.append(_admin.parseStr(newName))

    if len(values) == 0: return statusCode.SUCCESS

    return _admin.update("user", id, updates, values)

def verify(login:str, password:str) -> tuple[bool, statusCode]:
    login = _admin.parseStr(login)
    password = _admin.parseStr(password)

    conn = sqlite3.connect(_admin.databaseName)
    cursor = conn.cursor()

    retCode = statusCode.SUCCESS
    retStat = False
    try:
        cursor.execute(
            "SELECT password from user WHERE login=?",
            (login,)
        )

        userData = cursor.fetchone()
        if userData: 
            retStat = password == userData[0]
        else:
            retCode = statusCode.NOT_EXIST

    except Exception as e:
        print(e)

    conn.close()

    return retStat, retCode

