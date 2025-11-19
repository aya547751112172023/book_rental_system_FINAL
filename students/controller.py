from fastapi import APIRouter, Depends, Request
from database import get_db_connection
from mysql.connector.connection import MySQLConnection

from .models import Student, Insert_Student, Delete_Student
from .services import (
    get_students,
    get_student_grades,
    get_student,
    insert_student,
    update_student,
    delete_student,
)

router = APIRouter(prefix="/students")


@router.get("/")
def api_get_students(conn: MySQLConnection = Depends(get_db_connection)):
    try:
        data = get_students(conn=conn)
        return {"data": data}
    except Exception as e:
        return {"message": "Error occurred while executing function", "error": str(e)}


@router.get("/grades")
def api_get_student_grades(conn: MySQLConnection = Depends(get_db_connection)):
    try:
        data = get_student_grades(conn=conn)
        return {"data": data}
    except Exception as e:
        return {"message": "Error occurred while executing function", "error": str(e)}


@router.post("/")
def api_insert_student(
    payload: Insert_Student, conn: MySQLConnection = Depends(get_db_connection)
):
    try:
        results = insert_student(conn=conn, payload=payload)
        return {"message": f"Student inserted with id: {results}"}
    except Exception as e:
        return {"message": "Error occurred while executing function", "error": str(e)}


@router.post("/id")
def api_get_student(
    payload: Delete_Student, conn: MySQLConnection = Depends(get_db_connection)
):
    try:
        data = get_student(conn=conn, payload=payload)
        return {"data": data}
    except Exception as e:
        return {"message": "Error occurred while executing function", "error": str(e)}


@router.patch("/")
def api_update_student(
    payload: Student, conn: MySQLConnection = Depends(get_db_connection)
):
    try:
        results = update_student(conn=conn, payload=payload)
        return {"message": f"Student updated with id: {results}"}
    except Exception as e:
        return {"message": "Error occurred while executing function", "error": str(e)}


@router.delete("/")
def api_delete_student(
    payload: Delete_Student, conn: MySQLConnection = Depends(get_db_connection)
):
    try:
        results = delete_student(conn=conn, payload=payload)
        return {"message": f"{results} row/s deleted"}
    except Exception as e:
        return {"message": "Error occurred while executing function", "error": str(e)}
