from fastapi import APIRouter, Depends
from database import get_db_connection
from mysql.connector.connection import MySQLConnection


from .models import (
    Insert_Book, 
    Delete_Book, 
    Update_Book, 
    Insert_Rental, 
    Delete_Rental,
    Insert_User,
    Insert_Payment 
)

from .services import (
    get_books,
    get_book_by_id,
    get_payments,
    insert_book,
    update_book,
    delete_book,
    rent_book,
    return_book,
    get_users,        
    insert_user,      # <--- Added
    get_user_history,
    get_rental_dashboard,
    get_overdue_report,
    process_payment,
    get_payments

      # <--- Added
)

router = APIRouter(prefix="/library")

# ==========================================
# BOOK ROUTES
# ==========================================

@router.get("/books")
def api_get_books(conn: MySQLConnection = Depends(get_db_connection)):
    try:
        data = get_books(conn=conn)
        return {"data": data}
    except Exception as e:
        return {"message": "Error fetching books", "error": str(e)}

@router.post("/books")
def api_insert_book(
    payload: Insert_Book, conn: MySQLConnection = Depends(get_db_connection)
):
    try:
        new_id = insert_book(conn=conn, payload=payload)
        return {"message": f"Book added with ID: {new_id}"}
    except Exception as e:
        return {"message": "Error adding book", "error": str(e)}

@router.post("/books/detail")
def api_get_book(
    payload: Delete_Book, conn: MySQLConnection = Depends(get_db_connection)
):
    try:
        data = get_book_by_id(conn=conn, payload=payload)
        return {"data": data}
    except Exception as e:
        return {"message": "Error fetching book", "error": str(e)}

@router.patch("/books")
def api_update_book(
    payload: Update_Book, conn: MySQLConnection = Depends(get_db_connection)
):
    try:
        affected = update_book(conn=conn, payload=payload)
        return {"message": f"{affected} book(s) updated"}
    except Exception as e:
        return {"message": "Error updating book", "error": str(e)}

@router.delete("/books")
def api_delete_book(
    payload: Delete_Book, conn: MySQLConnection = Depends(get_db_connection)
):
    try:
        affected = delete_book(conn=conn, payload=payload)
        return {"message": f"{affected} book(s) marked inactive"}
    except Exception as e:
        return {"message": "Error deleting book", "error": str(e)}

# ==========================================
# RENTAL ROUTES
# ==========================================

@router.post("/rent")
def api_rent_book(
    payload: Insert_Rental, conn: MySQLConnection = Depends(get_db_connection)
):
    """Rents a book to a user and decreases stock"""
    try:
        rental_id = rent_book(conn=conn, payload=payload)
        return {"message": f"Rental successful. Rental ID: {rental_id}"}
    except Exception as e:
        return {"message": "Error processing rental", "error": str(e)}

@router.post("/return")
def api_return_book(
    payload: Delete_Rental, conn: MySQLConnection = Depends(get_db_connection)
):
    """Returns a book and increases stock"""
    try:
        msg = return_book(conn=conn, payload=payload)
        return {"message": msg}
    except Exception as e:
        return {"message": "Error processing return", "error": str(e)}

# ==========================================
# USER ROUTES (NEW)
# ==========================================

@router.get("/users")
def api_get_users(conn: MySQLConnection = Depends(get_db_connection)):
    """Fetch all registered users"""
    try:
        data = get_users(conn=conn)
        return {"data": data}
    except Exception as e:
        return {"message": "Error fetching users", "error": str(e)}

@router.post("/users")
def api_insert_user(
    payload: Insert_User, conn: MySQLConnection = Depends(get_db_connection)
):
    """Register a new user"""
    try:
        new_id = insert_user(conn=conn, payload=payload)
        return {"message": f"User added successfully with ID: {new_id}"}
    except Exception as e:
        return {"message": "Error adding user", "error": str(e)}

@router.get("/users/{user_id}/history")
def api_get_user_history(
    user_id: int, conn: MySQLConnection = Depends(get_db_connection)
):
    """See all books a specific user has ever rented"""
    try:
        data = get_user_history(conn=conn, user_id=user_id)
        if not data:
            return {"message": "No rental history found for this user."}
        return {"data": data}
    except Exception as e:
        return {"message": "Error fetching history", "error": str(e)}
    


# ==========================================
# OPERATIONS ROUTES
# ==========================================

@router.get("/operations/dashboard")
def api_rental_dashboard(conn: MySQLConnection = Depends(get_db_connection)):
    """General Operations: See all rentals, statuses, and potential fines"""
    try:
        data = get_rental_dashboard(conn=conn)
        return {"data": data}
    except Exception as e:
        return {"message": "Error fetching dashboard", "error": str(e)}

@router.get("/operations/overdue")
def api_overdue_tracking(conn: MySQLConnection = Depends(get_db_connection)):
    """Overdue Tracking: Only lists items that are late and calculates total fines"""
    try:
        data = get_overdue_report(conn=conn)
        
        if not data:
            return {"message": "Great news! No overdue items found."}

        
        total_fines = sum(item['fine_amount'] for item in data)

        return {
            "summary": f"Alert: {len(data)} items are overdue. Total Fines: {total_fines}",
            "data": data
        }
    except Exception as e:
        return {"message": "Error fetching overdue report", "error": str(e)}
    
    # ==========================================
# PAYMENT ROUTES
# ==========================================

@router.post("/payments")
def api_pay_fine(
    payload: Insert_Payment, conn: MySQLConnection = Depends(get_db_connection)
):
    """Record a payment for a specific rental"""
    try:
        payment_id = process_payment(conn=conn, payload=payload)
        return {"message": f"Payment recorded successfully. Payment ID: {payment_id}"}
    except Exception as e:
        return {"message": "Error processing payment", "error": str(e)}

@router.get("/payments")
def api_get_payments(conn: MySQLConnection = Depends(get_db_connection)):
    """See the history of all payments made"""
    try:
        data = get_payments(conn=conn)
        return {"data": data}
    except Exception as e:
        return {"message": "Error fetching payments", "error": str(e)}