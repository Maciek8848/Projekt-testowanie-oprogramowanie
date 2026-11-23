from . import _admin
from ._admin import statusCode
import sqlite3

def create(autor_id:int, content:str) -> tuple[int, statusCode]:
    return _admin.create(
        "paper", 
        ["id_autor", "content"],
        [autor_id, content]
    )

def read(ids:list[int]|None=None, content:bool=True, autor_id:bool=True) -> list:
    colm=[]
    if(content): colm.append("content")
    if(autor_id): colm.append("id_autor")
    return _admin.read("paper", ids, colm)

def delete(id:int) -> statusCode:
    return _admin.delete("paper", id)

def update(id:int, newContent:str=None, newAutorId:int=None) -> statusCode:
    updates = []
    values = []

    if newContent is not None:
        updates.append("content = ?")
        values.append(newContent)

    if newAutorId is not None:
        updates.append("id_autor = ?")
        values.append(newAutorId)

    if len(values) == 0: return statusCode.SUCCESS

    return _admin.update("user", id, updates, values)

def readOf(autor_id:int|None=None) -> list[int]:
    where = "1"
    val = []
    if not autor_id is None: 
        where="id_autor=?"
        val = [autor_id]
    return _admin.readId("paper", "id_autor=?", val)