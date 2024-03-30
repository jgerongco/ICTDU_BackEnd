# model/categories.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db

AdminRouter = APIRouter(tags=["Admin"])

# CRUD operations

@AdminRouter.get("/admin/", response_model=list)
async def read_categories(
    db=Depends(get_db)
):
    query = "SELECT admin_ID, firstname, lastname, password FROM admin"
    db[0].execute(query)
    categories = [{"admin_ID": category[0], "firstname": category[1], "lastname": category[2], "password": category[3]} for category in db[0].fetchall()]
    return categories

@AdminRouter.get("/admin/{admin_ID}", response_model=dict)
async def read_admin(
    admin_ID: int, 
    db=Depends(get_db)
):
    query = "SELECT admin_ID, firstname, lastname, password FROM admin WHERE admin_id = %s"
    db[0].execute(query, (admin_ID,))
    category = db[0].fetchone()
    if category:
        return {"admin_id": category[0], "firstname": category[1], "lastname": category[2], "password": category[3]}
    raise HTTPException(status_code=404, detail="Admin not found")

@AdminRouter.post("/admin/", response_model=dict)
async def create_admin(
    admin_ID: int,
    firstname: str = Form(...), 
    lastname: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):
    query = "INSERT INTO admin (admin_ID, firstname, lastname, password) VALUES (%s,%s,%s,%s)"
    db[0].execute(query, (admin_ID, firstname, lastname, password))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_admin_ID = db[0].fetchone()[0]
    db[1].commit()

    return {"admin_ID": new_admin_ID, "firstname": firstname, "lastname": lastname, "password": password}

@AdminRouter.put("/admin/{admin_id}", response_model=dict)
async def update_admin(
    admin_ID: int,
    firstname: str = Form(...),
    lastname: str = Form(...),
    db=Depends(get_db)
):
    # Update category information in the database 
    query = "UPDATE admin SET firstname = %s, lastname = %s WHERE admin_id = %s"
    db[0].execute(query, (firstname, lastname, admin_ID))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Admin updated successfully"}
    
    # If no rows were affected, category not found
    raise HTTPException(status_code=404, detail="Admin not found")

@AdminRouter.delete("/admin/{admin_id}", response_model=dict)
async def delete_admin(
    admin_ID: int,
    db=Depends(get_db)
):
    try:
        # Check if the category exists
        query_check_category = "SELECT admin_ID FROM admin WHERE admin_ID = %s"
        db[0].execute(query_check_category, (admin_ID,))
        existing_category = db[0].fetchone()

        if not existing_category:
            raise HTTPException(status_code=404, detail="Admin not found")

        # Delete the category
        query_delete_category = "DELETE FROM admin WHERE admin_ID = %s"
        db[0].execute(query_delete_category, (admin_ID,))
        db[1].commit()

        return {"message": "Admin deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()

