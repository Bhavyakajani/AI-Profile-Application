from fastapi import FastAPI
from profile_app.routers import profile, user, auth
from contextlib import asynccontextmanager
from profile_app.database.connection import db_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_connection._connect()
    yield
    await db_connection.close()


app = FastAPI(lifespan=lifespan)
"""Running on port 8001 by --port 8001"""

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(user.router)
