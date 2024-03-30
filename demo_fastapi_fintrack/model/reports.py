# model/categories.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db

ReportsRouter = APIRouter(tags=["Reports"])

# CRUD operations

@ReportsRouter.get("/reports/", response_model=list)
async def read_reports(
    db=Depends(get_db)
):
    query = "SELECT report_id, user_id, firstname, lastname, violation FROM reports"
    db[0].execute(query)
    categories = [{"report_id": category[0], 
                   "user_id": category[1], 
                   "firstname": category[2],
                   "lastname": category[3],
                   "violation": category[4]} for category in db[0].fetchall()]
    return categories

@ReportsRouter.get("/reports/{report_id}", response_model=dict)
async def read_reports(
    report_id: int, 
    db=Depends(get_db)
):
    query = "SELECT report_id, user_id, firstname, lastname, violation FROM reports WHERE report_id = %s"
    db[0].execute(query, (report_id,))
    category = db[0].fetchone()
    if category:
        return {"report_id": category[0], 
                   "user_id": category[1], 
                   "firstname": category[2],
                   "lastname": category[3],
                   "violation": category[4]}
    raise HTTPException(status_code=404, detail="Report not found")

@ReportsRouter.post("/reports/", response_model=dict)
async def create_reports(
    report_id: int,
    user_id: int,
    firstname: str = Form(...),
    lastname: str = Form(...),  
    violation: str = Form(...),
    db=Depends(get_db)
):
    query = "INSERT INTO reports (report_id, user_id, firstname, lastname, violation) VALUES (%s,%s,%s,%s,%s)"
    db[0].execute(query, (report_id, user_id, firstname, lastname, violation))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_report_id = db[0].fetchone()[0]
    db[1].commit()

    return {"report_id": new_report_id, "user_id": user_id, "firstname": firstname, "lastname": lastname, "violation": violation,}

@ReportsRouter.put("/reports/{report_id}", response_model=dict)
async def update_reports(
    report_id: int,
    user_id: int,
    firstname: str = Form(...),
    lastname: str = Form(...),  
    violation: str = Form(...),
    db=Depends(get_db)
):
    # Update category information in the database 
    query = "UPDATE reports SET user_id = %s, firstname = %s, lastname = %s, violation = %s WHERE report_id = %s"
    db[0].execute(query, (user_id, firstname, lastname, violation, report_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Reports updated successfully"}
    
    # If no rows were affected, category not found
    raise HTTPException(status_code=404, detail="Report not found")

@ReportsRouter.delete("/reports/{report_id}", response_model=dict)
async def reports(
    report_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the category exists
        query_check_category = "SELECT report_id FROM reports WHERE report_id = %s"
        db[0].execute(query_check_category, (report_id,))
        existing_category = db[0].fetchone()

        if not existing_category:
            raise HTTPException(status_code=404, detail="Report not found")

        # Delete the category
        query_delete_category = "DELETE FROM reports WHERE report_id = %s"
        db[0].execute(query_delete_category, (report_id,))
        db[1].commit()

        return {"message": "Report deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()

