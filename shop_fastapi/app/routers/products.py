from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import Product, Category
from sqlalchemy import insert, select, update
from app.schemas import CreateProduct

from slugify import slugify

# check user before crud products becouse need admin permission for this
from app.routers.auth import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

session = Annotated[AsyncSession, Depends(get_db)]
current_user_dep = Annotated[dict, Depends(get_current_user)]


@router.get("/")
async def all_products(db: session):
    products = await db.scalars(
        select(Product).where(Product.is_active == True, Product.stock > 0)
    )
    if products is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no product"
        )
    return products.all()


@router.post("/create")
async def create_product(
    db: session,
    product: CreateProduct,
    get_user: current_user_dep,
):
    if get_user.get("is_admin") or get_user.get("is_supplier"):
        await db.execute(
            insert(Product).values(
                name=product.name,
                description=product.description,
                slug=slugify(product.name),
                price=product.price,
                image_url=product.image_url,
                stock=product.stock,
                supplier_id=get_user.get("id"),
                rating=0.0,
                categories_id=product.category,
            )
        )
        await db.commit()
        return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to use this method",
        )


@router.get("/{category_slug}")
async def product_by_category(db: session, category_slug: str):
    category = await db.scalar(select(Category).where(Category.slug == category_slug))
    if not category_slug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    subcategories_ids = await db.scalars(
        select(Category.id).where(Category.parent_id == category.id)
    )
    categories_ids = [category.id] + subcategories_ids.all()
    products = await db.scalars(
        select(Product).where(
            Product.categories_id.in_(categories_ids),
            Product.is_active == True,
            Product.stock > 0,
        )
    )
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no product"
        )
    return products.all()


@router.get("/detail/{product_slug}")
async def product_detail(db: session, product_slug: str):
    product = await db.scalar(select(Product).where(Product.slug == product_slug))
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no product"
        )
    return product


@router.put("/detail/{product_slug}")
async def update_product(
    db: session,
    product_slug: str,
    update_product_model: CreateProduct,
    get_user: current_user_dep,
):
    product_update = await db.scalar(
        select(Product).where(Product.slug == product_slug)
    )
    if product_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not exist product with this product_slug",
        )
    if get_user.get("is_admin") or get_user.get("is_supplier"):
        if get_user.get("id") == product_update.supplier_id or get_user.get("is_admin"):
            await db.execute(
                update(Product)
                .where(Product.slug == product_slug)
                .values(
                    name=update_product_model.name,
                    description=update_product_model.description,
                    price=update_product_model.price,
                    image_url=update_product_model.image_url,
                    stock=update_product_model.stock,
                    categories_id=update_product_model.category,
                    slug=slugify(update_product_model.name),
                )
            )
            await db.commit()
            return {
                "status_code": status.HTTP_200_OK,
                "transaction": "Product update is successful",
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to use this method",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to use this method",
        )


@router.delete("/delete/{product_slug}")
async def delete_product(
    db: session,
    product_slug: str,
    get_user: current_user_dep,
):
    product_delete = await db.scalar(select(Product).where(Product.slug == product_slug))
    if product_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no product found",
        )
    if get_user.get("is_admin") or get_user.get("is_supplier"):
        if get_user.get("id") == product_delete.supplier_id or get_user.get("is_admin"):
            await db.execute(
                update(Product)
                .where(Product.slug == product_slug)
                .values(is_active=False)
            )
            await db.commit()
            return {
                "status_code": status.HTTP_200_OK,
                "transaction": "Product delete is successful",
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You must be admin user for this",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You must be admin user for this",
        )
