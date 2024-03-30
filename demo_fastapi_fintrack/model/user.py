# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import bcrypt

UserRouter = APIRouter(tags=["User"])

# CRUD operations

@UserRouter.get("/user/", response_model=list)
async def read_users(
    db=Depends(get_db)
):
    query = "SELECT user_id, student_id, firstname, lastname, email, password  FROM user"
    db[0].execute(query)
    users = [{"user_id": user[0], 
              "student_id": user[1],
              "firstname": user[2],
              "lastname": user[3],
              "email": user[4],
              "password": user[5]} for user in db[0].fetchall()]
    return users

@UserRouter.get("/user/{user_id}", response_model=dict)
async def read_user(
    user_id: int, 
    db=Depends(get_db)
):
    query = "SELECT user_id, student_id, firstname, lastname, email, password  FROM user WHERE user_id = %s"
    db[0].execute(query, (user_id,))
    user = db[0].fetchone()
    if user:
        return {"user_id": user[0], 
              "student_id": user[1],
              "firstname": user[2],
              "lastname": user[3],
              "email": user[4],
              "password": user[5]}
    raise HTTPException(status_code=404, detail="User not found")

@UserRouter.post("/user/", response_model=dict)
async def create_user(
    user_id: int,
    student_id: int,
    firstname: str = Form(...),
    lastname: str = Form(...),  
    email: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    hashed_password = hash_password(password)

    query = "INSERT INTO user (user_id, student_id, firstname, lastname, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
    db[0].execute(query, (user_id, student_id, firstname, lastname, email, hashed_password))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"user_id": new_user_id, 
            "student_id": student_id,
            "firstname": firstname,
            "lastname": lastname,
            "email": email
            }

@UserRouter.put("/user/{user_id}", response_model=dict)
async def update_user(
    user_id: int,
    student_id: int,
    firstname: str = Form(...),
    lastname: str = Form(...),  
    email: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    hashed_password = hash_password(password)

    # Update user information in the database 
    query = "UPDATE user SET student_id = %s, firstname = %s, lastname = %s, email = %s, password = %s WHERE user_id = %s"
    db[0].execute(query, (student_id, firstname, lastname, email, hashed_password, user_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "User updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="User not found")

@UserRouter.delete("/user/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT user_id FROM user WHERE user_id = %s"
        db[0].execute(query_check_user, (user_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        query_delete_user = "DELETE FROM user WHERE user_id = %s"
        db[0].execute(query_delete_user, (user_id,))
        db[1].commit()

        return {"message": "User deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()

# Password hashing function using bcrypt
def hash_password(password: str):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Decode bytes to string for storage
