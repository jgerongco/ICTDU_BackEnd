# model/categories.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db

ScheduleRouter = APIRouter(tags=["Schedule"])

# CRUD operations

@ScheduleRouter.get("/schedule/", response_model=list)
async def read_schedule(
    db=Depends(get_db)
):
    query = "SELECT schedule_id, reservation_id, user_id, firstname, lastname, email, faculty_in_charge, number_of_people, reservation_date, purpose FROM schedule"
    db[0].execute(query)
    categories = [{"schedule_id": category[0], 
                   "reservation_id": category[1],
                   "user_id": category[2],
                   "firstname": category[3],
                   "lastname": category[4],
                   "email": category[5],
                   "faculty_in_charge": category[6],  
                   "number_of_people": category[7],
                   "reservation_date": category[8],
                   "purpose": category[9]}for category in db[0].fetchall()]
    return categories

@ScheduleRouter.get("/schedule/{schedule_id}", response_model=dict)
async def read_schedule(
    schedule_id: int, 
    db=Depends(get_db)
):
    query = "SELECT schedule_id, reservation_id, user_id, firstname, lastname, email, faculty_in_charge, number_of_people, reservation_date, purpose FROM schedule WHERE schedule_id = %s"
    db[0].execute(query, (schedule_id,))
    category = db[0].fetchone()
    if category:
        return {"schedule_id": category[0], 
                   "reservation_id": category[1],
                   "user_id": category[2],
                   "firstname": category[3],
                   "lastname": category[4],
                   "email": category[5],
                   "faculty_in_charge": category[6],  
                   "number_of_people": category[7],
                   "reservation_date": category[8],
                   "purpose": category[9]}
    raise HTTPException(status_code=404, detail="Category not found")

@ScheduleRouter.post("/schedule/", response_model=dict)
async def create_schedule(
    schedule_id: int,
    reservation_id: int,
    user_id: int,
    number_of_people: int,
    firstname: str = Form(...), 
    lastname: str = Form(...), 
    email: str = Form(...), 
    faculty_in_charge: str = Form(...),
    reservation_date: str = Form(...),   
    purpose: str = Form(...),  
    db=Depends(get_db)
):
    query = "INSERT INTO schedule (schedule_id, reservation_id, user_id, number_of_people, firstname, lastname, email, faculty_in_charge, reservation_date, purpose) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    db[0].execute(query, (schedule_id, reservation_id, user_id, number_of_people, firstname, lastname, email, faculty_in_charge, reservation_date, purpose))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_schedule_id = db[0].fetchone()[0]
    db[1].commit()

    return {"schedule_id": schedule_id, "reservation_id": reservation_id, "user_id": user_id, "firstname": firstname, "lastname": lastname, "email": email, "faculty_in_charge": faculty_in_charge, "number_of_people": number_of_people, "reservation_date": reservation_date, "purpose": purpose}

@ScheduleRouter.put("/schedule/{schedule_id}", response_model=dict)
async def update_schedule(
    schedule_id: int,
    reservation_id: int,
    user_id: int,
    number_of_people: int,
    firstname: str = Form(...), 
    lastname: str = Form(...), 
    email: str = Form(...), 
    faculty_in_charge: str = Form(...),
    reservation_date: str = Form(...),   
    purpose: str = Form(...), 
    db=Depends(get_db)
):
    # Update category information in the database 
    query = "UPDATE schedule SET reservation_id = %s, user_id = %s, number_of_people = %s, firstname = %s, lastname = %s, email = %s, faculty_in_charge = %s, reservation_date = %s, purpose = %s WHERE schedule_id = %s "
    db[0].execute(query, (reservation_id, user_id, number_of_people, firstname, lastname, email, faculty_in_charge, reservation_date, purpose, schedule_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Schedule updated successfully"}
    
    # If no rows were affected, category not found
    raise HTTPException(status_code=404, detail="Schedule not found")

@ScheduleRouter.delete("/schedule/{schedule_id}", response_model=dict)
async def delete_category(
    schedule_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the category exists
        query_check_category = "SELECT schedule_id FROM schedule WHERE schedule_id = %s"
        db[0].execute(query_check_category, (schedule_id,))
        existing_category = db[0].fetchone()

        if not existing_category:
            raise HTTPException(status_code=404, detail="Schedule not found")

        # Delete the category
        query_delete_category = "DELETE FROM schedule WHERE schedule_id = %s"
        db[0].execute(query_delete_category, (schedule_id,))
        db[1].commit()

        return {"message": "Schedule deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()

