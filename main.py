from fastapi import FastAPI
from configs import config
from routers import roles, users, bodegas, clientes, contratos, costos, embarque, empresas, ganancias, productoras, productos, seguros, ventas

from db.client import get_cursor

app = FastAPI()
app.include_router(roles.router)
app.include_router(users.router)
app.include_router(bodegas.router)
app.include_router(clientes.router)
app.include_router(contratos.router)
app.include_router(costos.router)
app.include_router(embarque.router)
app.include_router(empresas.router)
app.include_router(ganancias.router)
app.include_router(productoras.router)
app.include_router(productos.router)
app.include_router(seguros.router)
app.include_router(ventas.router)


@app.get("/")
async def root():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM CLIENTES_LOCALES")
    return cursor.fetchall()