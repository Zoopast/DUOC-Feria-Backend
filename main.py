from fastapi import FastAPI
from configs import config
from routers import roles, users, bodegas, clientes, contratos, costos, embarque, empresas, ganancias, productoras, productos, seguros, ventas
from fastapi.middleware.cors import CORSMiddleware

from db.client import get_cursor

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {"message": "Hello World"}