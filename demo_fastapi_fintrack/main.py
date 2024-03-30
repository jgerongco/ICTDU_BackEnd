# main.py
from fastapi import FastAPI
from model.admin import AdminRouter
from model.history import HistoryRouter
from model.reports import ReportsRouter
from model.reservation import ReservationRouter
from model.schedule import ScheduleRouter
from model.user import UserRouter

app = FastAPI()

# Include CRUD routes from modules
app.include_router(UserRouter, prefix="/api")
app.include_router(AdminRouter, prefix="/api")
app.include_router(HistoryRouter, prefix="/api")
app.include_router(ReportsRouter, prefix="/api")
app.include_router(ReservationRouter, prefix="/api")
app.include_router(ScheduleRouter, prefix="/api")