from fastapi import FastAPI
from configs import config

app = FastAPI()


from db.client import get_cursor


@app.get("/")
async def root():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM CLIENTES_LOCALES")
    return cursor.fetchall()