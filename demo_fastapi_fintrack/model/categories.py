# model/categories.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db

CategoriesRouter = APIRouter(tags=["Categories"])

# CRUD operations

@CategoriesRouter.get("/categories/", response_model=list)
async def read_categories(
    db=Depends(get_db)
):
    query = "SELECT id, name FROM categories"
    db[0].execute(query)
    categories = [{"id": category[0], "name": category[1]} for category in db[0].fetchall()]
    return categories

@CategoriesRouter.get("/categories/{category_id}", response_model=dict)
async def read_category(
    category_id: int, 
    db=Depends(get_db)
):
    query = "SELECT id, name FROM categories WHERE id = %s"
    db[0].execute(query, (category_id,))
    category = db[0].fetchone()
    if category:
        return {"id": category[0], "name": category[1]}
    raise HTTPException(status_code=404, detail="Category not found")

@CategoriesRouter.post("/categories/", response_model=dict)
async def create_category(
    name: str = Form(...), 
    db=Depends(get_db)
):
    query = "INSERT INTO categories (name) VALUES (%s)"
    db[0].execute(query, (name))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_category_id = db[0].fetchone()[0]
    db[1].commit()

    return {"id": new_category_id, "name": name}

@CategoriesRouter.put("/categories/{category_id}", response_model=dict)
async def update_category(
    category_id: int,
    name: str = Form(...),
    db=Depends(get_db)
):
    # Update category information in the database 
    query = "UPDATE categories SET name = %s WHERE id = %s"
    db[0].execute(query, (name, category_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Category updated successfully"}
    
    # If no rows were affected, category not found
    raise HTTPException(status_code=404, detail="Category not found")

@CategoriesRouter.delete("/categories/{category_id}", response_model=dict)
async def delete_category(
    category_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the category exists
        query_check_category = "SELECT id FROM categories WHERE id = %s"
        db[0].execute(query_check_category, (category_id,))
        existing_category = db[0].fetchone()

        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")

        # Delete the category
        query_delete_category = "DELETE FROM categories WHERE id = %s"
        db[0].execute(query_delete_category, (category_id,))
        db[1].commit()

        return {"message": "Category deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()

