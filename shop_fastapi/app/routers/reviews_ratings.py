from fastapi import HTTPException, APIRouter, Depends, status
from app.backend.db_depends import get_db
from app.routers.auth import get_current_user
from app.models import User, Category, Rating, Review, Product
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import CreateReviewWithRating
from typing import Annotated

router = APIRouter(prefix="/reviews", tags=["review"])
SessionDep = Annotated[AsyncSession, Depends(get_db)]
CurrentUserDep = Annotated[dict, Depends(get_current_user)]


@router.get("/all_reviews")
async def all_reviews(db: SessionDep):
    all_reviews = await db.scalars(select(Review))
    reviews = all_reviews.all()
    if not reviews:
        return {"Reviews not exists"}
    return {"status_code": status.HTTP_200_OK, "reviews": reviews}


@router.get("/{product_slug}")
async def product_reviews(product_slug: str, db: SessionDep):
    product = await db.scalar(select(Product).where(Product.slug == product_slug))
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no product with this product_slug",
        )
    reviews = await db.scalars(
        select(Review)
        .where(Review.product_id == product.id, Review.is_active==True))
    reviews = list(reviews)

    if not reviews:
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "This product has not review",
        }
    response = []
    for review in reviews:
        rating = await db.scalar(
            select(Rating)
            .where(Rating.id == review.rating_id, Rating.is_active==True))
        
        response.append(
            {
                "user_id": review.user_id,
                "review_id": review.id,
                "review_comment": review.comment,
                "rating_id": rating.id,
                "rating_grade": rating.grade,
            }
        )
    return {
        "status_code": status.HTTP_200_OK,
        "Reviews": response if response else "This product has not active review",
    }


@router.post("/")
async def add_review(
    get_user: CurrentUserDep,
    db: SessionDep,
    review_model: CreateReviewWithRating,
):
    product = await db.scalar(
        select(Product).where(Product.id == review_model.product_id)
    )
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no product with this product_id",
        )
    if get_user.get("is_customer"):
        rating = await db.execute(
            insert(Rating)
            .values(
                product_id=review_model.product_id,
                grade=review_model.grade,
                user_id=get_user.get("id"),
            )
            .returning(Rating.id)
        )
        await db.execute(
            insert(Review).values(
                user_id=get_user.get("id"),
                product_id=review_model.product_id,
                rating_id=rating.scalar_one(),
                comment=review_model.comment,
            )
        )

        ratings = await db.scalars(
            select(Rating.grade).where(
                Rating.product_id == product.id, Rating.is_active == True
            )
        )
        ratings = list(ratings)
        product.rating = sum(ratings) / len(ratings)
        await db.commit()
        return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Reviews are available to buyers only",
        )


@router.delete("/{review_id}")
async def delete_review(review_id: int, get_user: CurrentUserDep, db: SessionDep):
    review = await db.scalar(select(Review).where(Review.id == review_id))
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no review with this review_id",
        )
    rating_id = review.rating_id
    if get_user.get("is_admin"):
        await db.execute(
            update(Review).where(Review.id == review_id).values(is_active=False)
        )
        await db.execute(
            update(Rating).where(Rating.id == rating_id).values(is_active=False)
        )

        product = await db.scalar(
            select(Product).where(Product.id == review.product_id)
        )
        ratings = await db.scalars(
            select(Rating.grade).where(
                Rating.product_id == product.id, Rating.is_active == True
            )
        )
        ratings = list(ratings)
        product.rating = sum(ratings) / len(ratings) if ratings else 0

        await db.commit()
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Review delete is successful",
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You must be admin user for this",
        )
