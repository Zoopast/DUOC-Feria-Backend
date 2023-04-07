from fastapi import APIRouter, HTTPException
from db.client import get_cursor
from db.models.producto import Producto

router = APIRouter(
    prefix="/productos",
    tags=["productos"],
    responses={404: {"description": "Not found"}},
)

con, connection = get_cursor()

@router.get("/")
async def get_productos():
    con.execute("SELECT * FROM PRODUCTOS")
    result = con.fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return [{"id": row[0], "nombre": row[1]} for row in result]

@router.get("/{id_producto}")
async def get_producto(id_producto: int):
    con.execute("SELECT * FROM PRODUCTOS WHERE id = :id", {"id": id_producto})
    result = con.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"id": result[0], "nombre": result[1]}

@router.post("/")
async def create_producto(producto: Producto):
    con.execute("""INSERT INTO PRODUCTOS VALUES (:id, :nombre)
                   VALUES (:nombre) 
                """, )
    connection.commit()
    return {"message": "Producto creado correctamente"}

@router.put("/{id_producto}")
async def update_producto(id_producto: int, producto: Producto):
    con.execute("UPDATE PRODUCTOS SET nombre = :nombre WHERE id = :id", {"nombre": producto.nombre, "id": id_producto})
    con.commit()
    return {"message": "Producto actualizado correctamente"}

@router.delete("/{id_producto}")
async def delete_producto(id_producto: int):
    con.execute("DELETE FROM PRODUCTOS WHERE id = :id", {"id": id_producto})
    con.commit()
    return {"message": "Producto eliminado correctamente"}