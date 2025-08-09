from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import Product, Category
from sqlalchemy import insert, select, update
from app.schemas import CreateProduct

from slugify import slugify

router = APIRouter(prefix='/products', tags=['products'])

session = Annotated[Session, Depends(get_db)]

@router.get('/')
async def all_products(db: session):
    products = db.scalars(
        select(Product)
        .where(Product.is_active == True, 
               Product.stock > 0)).all()
    if products is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no product'
        )
    return products


@router.post('/create')
async def create_product(db: session, product: CreateProduct):
    db.execute(insert(Product).values(
        name = product.name,
        description = product.description,
        slug = slugify(product.name),
        price = product.price,
        image_url = product.image_url,
        stock = product.stock,
        rating = 0.0,
        categories_id=product.category
        
    ))
    db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get('/{category_slug}')
async def product_by_category(db: session, category_slug: str):
    category = db.scalar(select(Category).where(Category.slug == category_slug))
    if not category_slug:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Category not found")
    subcategories_ids = db.scalars(select(Category.id).where(Category.parent_id == category.id)).all()
    categories_ids = [category.id] + subcategories_ids
    products = db.scalars(
        select(Product)
        .where(Product.categories_id.in_(categories_ids),
        Product.is_active == True,
        Product.stock > 0)
        ).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are no product")
    return products


@router.get('/detail/{product_slug}')
async def product_detail(db: session, product_slug: str):
    product = db.scalar(select(Product).where(Product.slug == product_slug))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='There are no product') 
    return product


@router.put('/detail/{product_slug}')
async def update_product(db: session, product_slug: str, update_product: CreateProduct):
    product = db.scalar(select(Product).where(Product.slug == product_slug))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail='Not exist product with this product_slug') 
    db.execute(update(Product).where(Product.slug == product_slug).values(
        name = update_product.name,
        description = update_product.description,
        price = update_product.price,
        image_url = update_product.image_url,
        stock = update_product.stock,
        categories_id = update_product.category
    ))
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        'transaction': 'Product update is successful'
    }


@router.delete('/delete/{product_slug}')
async def delete_product(db: session, product_slug:str):
    product = db.scalar(select(Product).where(Product.slug == product_slug))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail='Not exist product with this product_slug') 
    db.execute(update(Product).where(Product.slug == product_slug)
               .values(is_active=False))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product delete is successful'
    }