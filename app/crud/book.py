from sqlalchemy.orm import Session

from ..models.book import Book, BookImage
from ..schemas.book import BookCreate, BookUpdate


def get_book(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category: str | None = None,
    search: str | None = None,
) -> list[Book]:
    query = db.query(Book)

    if category:
        query = query.filter(Book.category == category)

    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))

    return query.offset(skip).limit(limit).all()


def count_books(
    db: Session,
    category: str | None = None,
    search: str | None = None,
) -> int:
    from sqlalchemy import func

    query = db.query(func.count(Book.id))

    if category:
        query = query.filter(Book.category == category)

    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))

    return query.scalar() or 0


def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(
        title=book.title,
        category=book.category,
        description=book.description,
        price=book.price,
        discount_price=book.discount_price,
    )
    db.add(db_book)
    db.flush()

    for img in book.images:
        db.add(
            BookImage(
                book_id=db_book.id,
                image_url=img.image_url,
                is_primary=img.is_primary,
            )
        )

    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book_update: BookUpdate) -> Book | None:
    db_book = get_book(db, book_id)
    if not db_book:
        return None

    payload = book_update.model_dump(exclude_unset=True)

    images = payload.pop("images", None)

    for field, value in payload.items():
        setattr(db_book, field, value)

    if images is not None:
        db.query(BookImage).filter(BookImage.book_id == book_id).delete()
        for img in images:
            db.add(
                BookImage(
                    book_id=book_id,
                    image_url=img.image_url,
                    is_primary=img.is_primary,
                )
            )

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book(db, book_id)
    if not db_book:
        return False

    db.delete(db_book)
    db.commit()
    return True