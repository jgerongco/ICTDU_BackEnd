# main.py
from fastapi import FastAPI
from model.users import UsersRouter
from model.categories import CategoriesRouter
from model.expenses import ExpensesRouter

app = FastAPI()

# Include CRUD routes from modules
app.include_router(UsersRouter, prefix="/api")
app.include_router(CategoriesRouter, prefix="/api")
app.include_router(ExpensesRouter, prefix="/api")