from . import _admin
from ._admin import statusCode
import sqlite3

def create(paper_id:int, autor_id:int, content:str) -> tuple[int, statusCode]:
    return _admin.create(
        "review", 
        ["id_paper","id_autor", "content"],
        [paper_id,autor_id, content]
    )

def read(ids:list[int]|None=None, content:bool=True, paper_id:bool=True, autor_id:bool=True) -> list:
    colm=[]
    if(content): colm.append("content")
    if(autor_id): colm.append("id_autor")
    if(paper_id): colm.append("id_paper")
    return _admin.read("review", ids, colm)

def delete(id:int) -> statusCode:
    return _admin.delete("review", id)

def update(id:int, newContent:str=None, newPaperId:int=None, newAutorId:int=None) -> statusCode:
    updates = []
    values = []

    if newContent is not None:
        updates.append("content = ?")
        values.append(newContent)

    if newAutorId is not None:
        updates.append("id_autor = ?")
        values.append(newAutorId)

    if newPaperId is not None:
            updates.append("id_paper = ?")
            values.append(newPaperId)

    if len(values) == 0: return statusCode.SUCCESS

    return _admin.update("review", id, updates, values)

def readOf(paper_id:int|None=None, autor_id:int|None=None):
    where = []
    val = []
    if not autor_id is None: 
        where.append("id_autor=?")
        val.append(autor_id)
    if not paper_id is None: 
        where.append("id_paper=?")
        val.append(paper_id)
    if len(where): where = " AND ".join(where)
    else: where = '1'
    return _admin.readId("paper", where, val)