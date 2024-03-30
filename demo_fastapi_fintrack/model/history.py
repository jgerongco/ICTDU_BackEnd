# model/categories.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db

HistoryRouter = APIRouter(tags=["History"])

# CRUD operations

@HistoryRouter.get("/history/", response_model=list)
async def read_history(
    db=Depends(get_db)
):
    query = "SELECT history_id, reservation_date, user_id, firstname, lastname, email, faculty_in_charge, purpose FROM history"
    db[0].execute(query)
    history = [{"history_id": category[0], "reservation_date": category[1], "user_id": category[2], "firstname": category[3], "lastname": category[4], "email": category[5], "faculty_in_charge": category[6],"purpose": category[7]} for category in db[0].fetchall()]
    return history

@HistoryRouter.get("/history/{history_id}", response_model=dict)
async def read_history(
    history_id: int, 
    db=Depends(get_db)
):
    query = "SELECT history_id, reservation_date, user_id, firstname, lastname, email, faculty_in_charge, purpose FROM history WHERE history_id = %s"
    db[0].execute(query, (history_id,))
    category = db[0].fetchone()
    if category:
        return {"history_id": category[0], "reservation_date": category[1], "user_id": category[2], "firstname": category[3], "lastname": category[4], "email": category[5], "faculty_in_charge": category[6],"purpose": category[7]}
    raise HTTPException(status_code=404, detail="Category not found")

@HistoryRouter.post("/history/", response_model=dict)
async def create_history(
    history_id: int,
    user_id: int,
    reservation_date: str = Form(...),
    firstname: str = Form(...),
    lastname: str = Form(...),
    email: str = Form(...),
    faculty_in_charge: str = Form(...),
    purpose: str = Form(...),
    db=Depends(get_db)
):
    query = "INSERT INTO history (history_id, user_id, reservation_date, firstname, lastname, email, faculty_in_charge, purpose) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    db[0].execute(query, (history_id, user_id, reservation_date, firstname, lastname, email, faculty_in_charge, purpose))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_category_id = db[0].fetchone()[0]
    db[1].commit()

    return {"history_id": history_id, "user_id": user_id, "reservation_date": reservation_date, "firstname": firstname, "lastname": lastname, "email": email,"faculty_in_charge": faculty_in_charge, "purpose": purpose}

@HistoryRouter.put("/history/{history_id}", response_model=dict)
async def update_history(
    history_id: int,
    user_id: int,
    reservation_date: str = Form(...),
    firstname: str = Form(...),
    lastname: str = Form(...),
    email: str = Form(...),
    faculty_in_charge: str = Form(...),
    purpose: str = Form(...),
    db=Depends(get_db)
):
    # Update category information in the database 
    query = "UPDATE history SET user_id = %s, reservation_date = %s, firstname = %s, lastname = %s, email = %s, faculty_in_charge = %s, purpose = %s  WHERE history_id = %s"
    db[0].execute(query, (user_id, reservation_date, firstname, lastname, email, faculty_in_charge, purpose, history_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "History updated successfully"}
    
    # If no rows were affected, category not found
    raise HTTPException(status_code=404, detail="History not found")

@HistoryRouter.delete("/history/{category_id}", response_model=dict)
async def delete_history(
    history_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the category exists
        query_check_category = "SELECT history_id FROM history WHERE history_id = %s"
        db[0].execute(query_check_category, (history_id,))
        existing_category = db[0].fetchone()

        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")

        # Delete the category
        query_delete_category = "DELETE FROM history WHERE history_id = %s"
        db[0].execute(query_delete_category, (history_id,))
        db[1].commit()

        return {"message": "History deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()

