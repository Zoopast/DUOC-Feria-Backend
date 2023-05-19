from fastapi import FastAPI
from routers import users, productos, seguros, productores, comerciantes, requerimientos
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:4200",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(productos.router)
app.include_router(seguros.router)
app.include_router(productores.router)
app.include_router(comerciantes.router)
app.include_router(requerimientos.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}