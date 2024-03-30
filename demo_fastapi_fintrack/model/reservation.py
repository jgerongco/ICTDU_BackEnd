# model/categories.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db

ReservationRouter = APIRouter(tags=["Reservation"])

# CRUD operations

@ReservationRouter.get("/reservation/", response_model=list)
async def read_reservation(
    db=Depends(get_db)
):
    query = "SELECT reservation_id, user_id, firstname, lastname, email, faculty_in_charge, number_of_people, reservation_date, purpose FROM reservation"
    db[0].execute(query)
    reservation = [{"reservation_id": category[0], 
                   "user_id": category[1],
                   "firstname": category[2],
                   "lastname": category[3],
                   "email": category[4],
                   "faculty_in_charge": category[5],
                   "number_of_people": category[6],  
                   "purpose": category[7] } for category in db[0].fetchall()]
    return reservation

@ReservationRouter.get("/reservation/{category_id}", response_model=dict)
async def read_reservation(
    reservation_id: int, 
    db=Depends(get_db)
):
    query = "SELECT reservation_id, user_id, firstname, lastname, email, faculty_in_charge, number_of_people, reservation_date, purpose FROM reservation WHERE reservation_id = %s"
    db[0].execute(query, (reservation_id,))
    category = db[0].fetchone()
    if category:
        return {"reservation_id": category[0], 
                   "user_id": category[1],
                   "firstname": category[2],
                   "lastname": category[3],
                   "email": category[4],
                   "faculty_in_charge": category[5],
                   "number_of_people": category[6],
                   "reservation_date": category[7],  
                   "purpose": category[8]}
    raise HTTPException(status_code=404, detail="Reservation not found")

@ReservationRouter.post("/reservation/", response_model=dict)
async def create_reservation(
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
    query = "INSERT INTO reservation (reservation_id, user_id, firstname, lastname, email, faculty_in_charge, number_of_people, reservation_date, purpose) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    db[0].execute(query, (reservation_id, user_id, firstname, lastname, email, faculty_in_charge, number_of_people, reservation_date, purpose))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_category_id = db[0].fetchone()[0]
    db[1].commit()

    return {"reservation_id": reservation_id, "user_id": user_id, "firstname": firstname, "lastname": lastname, "email": email, "faculty_in_charge": faculty_in_charge, "number_of_people": number_of_people, "reservation_date": reservation_date, "purpose": purpose}

@ReservationRouter.put("/reservation/{reservation_id}", response_model=dict)
async def update_reservation(
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
    query = "UPDATE reservation SET user_id = %s, number_of_people = %s, firstname = %s, lastname = %s, email = %s, faculty_in_charge = %s, reservation_date = %s, purpose = %s  WHERE reservation_id = %s"
    db[0].execute(query, (user_id, number_of_people, firstname, lastname, email, faculty_in_charge, reservation_date, purpose, reservation_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Reservation updated successfully"}
    
    # If no rows were affected, category not found
    raise HTTPException(status_code=404, detail="Reservation not found")

@ReservationRouter.delete("/reservation/{reservation_id}", response_model=dict)
async def delete_category(
    reservation_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the category exists
        query_check_category = "SELECT reservation_id FROM reservation WHERE reservation_id = %s"
        db[0].execute(query_check_category, (reservation_id,))
        existing_category = db[0].fetchone()

        if not existing_category:
            raise HTTPException(status_code=404, detail="Reservation not found")

        # Delete the category
        query_delete_category = "DELETE FROM reservation WHERE reservation_id = %s"
        db[0].execute(query_delete_category, (reservation_id,))
        db[1].commit()

        return {"message": "Reservation deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()

