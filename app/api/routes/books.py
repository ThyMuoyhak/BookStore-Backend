from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_current_user, get_db
from ...crud.book import count_books, create_book, delete_book, get_book, get_books, update_book
from ...models.user import User
from ...schemas.book import BookCreate, BookList, BookOut, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=BookList)
def list_books(
    skip: int = 0,
    limit: int = 100,
    category: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    total = count_books(db, category=category, search=search)
    items = get_books(db, skip=skip, limit=limit, category=category, search=search)
    return BookList(total=total, items=items)


@router.get("/{book_id}", response_model=BookOut)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book


@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_new_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_book(db, book)


@router.put("/{book_id}", response_model=BookOut)
def update_existing_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = update_book(db, book_id, book_update)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_book(db, book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )