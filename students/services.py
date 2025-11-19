from mysql.connector.connection import MySQLConnection
import students.models as models


def get_students(conn: MySQLConnection):
    cursor = conn.cursor()
    query = "SELECT * FROM students"
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def get_student_grades(conn: MySQLConnection):
    cursor = conn.cursor()
    query = "SELECT * FROM student_grades_view"
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def get_student(conn: MySQLConnection, payload: models.Delete_Student):
    cursor = conn.cursor()
    query = "SELECT * FROM students WHERE student_id = %s"
    values = (payload.student_id,)
    cursor.execute(query, values)
    results = cursor.fetchone()
    return results


def insert_student(conn: MySQLConnection, payload: models.Insert_Student):
    cursor = conn.cursor()
    query = "INSERT INTO students (full_name, year_level, department) VALUES (%s, %s, %s)"  # %s prevents sql injections
    values = (payload.full_name, payload.year_level, payload.department)
    cursor.execute(query, values)
    conn.commit()
    return cursor.lastrowid


def update_student(conn, payload: models.Student):
    cursor = conn.cursor()
    query = "UPDATE students SET full_name = %s, year_level = %s, department = %s WHERE student_id = %s"
    values = (
        payload.full_name,
        payload.year_level,
        payload.department,
        payload.student_id,
    )
    cursor.execute(query, values)
    conn.commit()
    return cursor.lastrowid


def delete_student(conn, payload: models.Delete_Student):
    cursor = conn.cursor()
    query = "DELETE FROM students WHERE student_id = %s"
    values = (payload.student_id,)  # comma is important when there is only 1 value
    cursor.execute(query, values)
    conn.commit()
    return cursor.rowcount
