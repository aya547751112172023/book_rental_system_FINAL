from mysql.connector.connection import MySQLConnection
from mysql.connector import Error
from fastapi import HTTPException
from . import models

# ==========================================
# BOOK SERVICES (CRUD)
# ==========================================

def get_books(conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    # UPDATED: Use JOIN to fetch Author/Genre names instead of just IDs
    query = """
        SELECT 
            b.id, 
            b.title, 
            a.name AS author, 
            c.name AS genre, 
            b.total_copies, 
            b.available_copies,
            b.is_active
        FROM books b
        LEFT JOIN authors a ON b.author_id = a.id
        LEFT JOIN categories c ON b.category_id = c.id
        WHERE b.is_active = TRUE
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

def get_book_by_id(conn: MySQLConnection, payload: models.Delete_Book):
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            b.id, 
            b.title, 
            a.name AS author, 
            c.name AS genre, 
            b.total_copies, 
            b.available_copies
        FROM books b
        LEFT JOIN authors a ON b.author_id = a.id
        LEFT JOIN categories c ON b.category_id = c.id
        WHERE b.id = %s
    """
    values = (payload.book_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    return result

def insert_book(conn: MySQLConnection, payload: models.Insert_Book):
    cursor = conn.cursor(dictionary=True)
    try:
        # STEP 1: Handle Author (Lookup ID or Create)
        cursor.execute("SELECT id FROM authors WHERE name = %s", (payload.author,))
        author_res = cursor.fetchone()
        
        if author_res:
            author_id = author_res['id']
        else:
            cursor.execute("INSERT INTO authors (name) VALUES (%s)", (payload.author,))
            author_id = cursor.lastrowid

        # STEP 2: Handle Category/Genre (Lookup ID or Create)
        cursor.execute("SELECT id FROM categories WHERE name = %s", (payload.genre,))
        cat_res = cursor.fetchone()
        
        if cat_res:
            category_id = cat_res['id']
        else:
            cursor.execute("INSERT INTO categories (name) VALUES (%s)", (payload.genre,))
            category_id = cursor.lastrowid

        # STEP 3: Insert Book using IDs
        query = """
        INSERT INTO books (title, author_id, category_id, total_copies, available_copies) 
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            payload.title, 
            author_id, 
            category_id, 
            payload.total_copies, 
            payload.total_copies
        )
        cursor.execute(query, values)
        conn.commit()
        new_id = cursor.lastrowid
        return new_id

    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
    finally:
        cursor.close()

def update_book(conn: MySQLConnection, payload: models.Update_Book):
    cursor = conn.cursor()
    updates = []
    params = []

    if payload.total_copies is not None:
        updates.append("total_copies = %s")
        params.append(payload.total_copies)
    
    if payload.is_active is not None:
        updates.append("is_active = %s")
        params.append(payload.is_active)
    
    if not updates:
        return 0

    query = f"UPDATE books SET {', '.join(updates)} WHERE id = %s"
    params.append(payload.book_id)

    cursor.execute(query, tuple(params))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    return affected

def delete_book(conn: MySQLConnection, payload: models.Delete_Book):
    cursor = conn.cursor()
    query = "UPDATE books SET is_active = FALSE WHERE id = %s"
    values = (payload.book_id,)
    cursor.execute(query, values)
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    return affected

# ==========================================
# RENTAL SERVICES (TRANSACTIONS)
# ==========================================

def rent_book(conn: MySQLConnection, payload: models.Insert_Rental):
    cursor = conn.cursor(dictionary=True)
    try:
        check_query = "SELECT available_copies FROM books WHERE id = %s FOR UPDATE"
        cursor.execute(check_query, (payload.book_id,))
        book = cursor.fetchone()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        if book['available_copies'] < 1:
            raise HTTPException(status_code=400, detail="No copies available")

        rent_query = "INSERT INTO rentals (user_id, book_id) VALUES (%s, %s)"
        cursor.execute(rent_query, (payload.user_id, payload.book_id))
        rental_id = cursor.lastrowid

        update_stock = "UPDATE books SET available_copies = available_copies - 1 WHERE id = %s"
        cursor.execute(update_stock, (payload.book_id,))

        conn.commit()
        return rental_id

    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

def return_book(conn: MySQLConnection, payload: models.Delete_Rental):
    cursor = conn.cursor(dictionary=True)
    try:
        find_query = "SELECT book_id, returned_at FROM rentals WHERE id = %s"
        cursor.execute(find_query, (payload.rental_id,))
        rental = cursor.fetchone()

        if not rental:
            raise HTTPException(status_code=404, detail="Rental ID not found")
        
        if rental['returned_at'] is not None:
            raise HTTPException(status_code=400, detail="Book already returned")

        return_query = "UPDATE rentals SET returned_at = NOW() WHERE id = %s"
        cursor.execute(return_query, (payload.rental_id,))

        update_stock = "UPDATE books SET available_copies = available_copies + 1 WHERE id = %s"
        cursor.execute(update_stock, (rental['book_id'],))

        conn.commit()
        return "Book returned successfully"

    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# ==========================================
# USER SERVICES (NEWLY ADDED)
# ==========================================

def get_users(conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM users"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

def insert_user(conn: MySQLConnection, payload: models.Insert_User):
    cursor = conn.cursor()
    try:
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        values = (payload.name, payload.email)
        cursor.execute(query, values)
        conn.commit()
        new_id = cursor.lastrowid
        return new_id
    except Error as e:
        conn.rollback()
        # Handle Duplicate Email Error
        if e.errno == 1062:
            raise HTTPException(status_code=400, detail="Email already exists")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

def get_user_history(conn: MySQLConnection, user_id: int):
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            b.title, 
            b.author_id, 
            r.rented_at, 
            r.returned_at,
            CASE 
                WHEN r.returned_at IS NULL THEN 'Available'
                ELSE 'Returned'
            END as status
        FROM rentals r
        JOIN books b ON r.book_id = b.id
        WHERE r.user_id = %s
        ORDER BY r.rented_at DESC
    """
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()
    cursor.close()
    return results

    # ==========================================
# OPERATIONS & TRACKING SERVICES
# ==========================================

def get_rental_dashboard(conn: MySQLConnection):
    """Gets the full list of all rentals with statuses and fines"""
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM view_rental_operations"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

def get_overdue_report(conn: MySQLConnection):
    """Gets ONLY the items that are overdue and have fines"""
    cursor = conn.cursor(dictionary=True)
    # We filter the SQL View to only show problems
    query = "SELECT * FROM view_rental_operations WHERE status = 'Overdue'"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

# ==========================================
# PAYMENT SERVICES
# ==========================================

def process_payment(conn: MySQLConnection, payload: models.Insert_Payment):
    cursor = conn.cursor(dictionary=True)
    try:
        # STEP 1: Get Rental Details (We need book_id and status)
        # We assume if you are paying, you are also returning the book now.
        check_query = "SELECT id, book_id, returned_at FROM rentals WHERE id = %s"
        cursor.execute(check_query, (payload.rental_id,))
        rental = cursor.fetchone()
        
        if not rental:
            raise HTTPException(status_code=404, detail="Rental ID not found")

        # STEP 2: Record the Payment
        sql_pay = """
            INSERT INTO payments (rental_id, amount, notes, payment_date) 
            VALUES (%s, %s, %s, NOW())
        """
        vals_pay = (payload.rental_id, payload.amount, payload.notes)
        cursor.execute(sql_pay, vals_pay)
        payment_id = cursor.lastrowid

        # STEP 3: Auto-Return the Book (If it hasn't been returned yet)
        if rental['returned_at'] is None:
            # A. Mark rental as Closed/Returned
            return_query = "UPDATE rentals SET returned_at = NOW() WHERE id = %s"
            cursor.execute(return_query, (payload.rental_id,))

            # B. Restock the Book
            stock_query = "UPDATE books SET available_copies = available_copies + 1 WHERE id = %s"
            cursor.execute(stock_query, (rental['book_id'],))

        conn.commit()
        return payment_id

    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

def get_payments(conn: MySQLConnection):
    """View all payment history"""
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT p.id, p.amount, p.payment_date, p.notes, 
               b.title, u.name as user_name
        FROM payments p
        JOIN rentals r ON p.rental_id = r.id
        JOIN books b ON r.book_id = b.id
        JOIN users u ON r.user_id = u.id
        ORDER BY p.payment_date DESC
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    return results