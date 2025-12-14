from pydantic import BaseModel
from typing import Optional

# ==========================================
# BOOK MODELS
# ==========================================

class Insert_Book(BaseModel):
    """Fields required to add a new book"""
    title: str
    author: str
    genre: str
    total_copies: int = 1

class Delete_Book(BaseModel):
    """Fields required to identify a book"""
    book_id: int

class Update_Book(BaseModel):
    """Fields allowed when updating a book"""
    book_id: int
    total_copies: Optional[int] = None
    is_active: Optional[bool] = None

class Book(Insert_Book, Delete_Book):
    """Combines ID (from Delete) + Data (from Insert)"""
    available_copies: int
    is_active: bool

# ==========================================
# RENTAL MODELS
# ==========================================

class Insert_Rental(BaseModel):
    """Data needed to rent a book"""
    user_id: int
    book_id: int

class Delete_Rental(BaseModel):
    """Data needed to return a book (using the unique rental ID)"""
    rental_id: int

    # ==========================================
# USER MODELS (ADDED THIS SECTION)
# ==========================================

class Insert_User(BaseModel):
    """Fields required to register a user"""
    name: str
    email: str

    # ==========================================
# PAYMENT MODELS (NEW)
# ==========================================

class Insert_Payment(BaseModel):
    rental_id: int
    amount: float
    notes: str = "Fine Payment"