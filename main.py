from fastapi import FastAPI
from configs import config
from routers import roles, users

from db.client import get_cursor

app = FastAPI()
app.include_router(roles.router)
app.include_router(users.router)


@app.get("/")
async def root():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM CLIENTES_LOCALES")
    return cursor.fetchall()