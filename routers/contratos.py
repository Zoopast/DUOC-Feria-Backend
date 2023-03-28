from fastapi import APIRouter, HTTPException
from db.client import get_cursor
from db.models.rol import Rol

router = APIRouter(
    prefix="/contratos",
    tags=["contratos"],
    responses={404: {"description": "Not found"}},
)

con, connection = get_cursor()

@router.get("/")
async def get_contratos():
    con.execute("SELECT * FROM rol")
    result = con.fetchall()
    print(result)
    if not result:
      raise HTTPException(status_code=404, detail="Rol no encontrado")
    return [{"id": row[0], "nombre": row[1]} for row in result]

@router.get("/{id}")
async def get_contrato(id: int):
    con.execute("SELECT * FROM rol WHERE id = :id", {"id": id})
    result = con.fetchone()
    if not result:
      raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"id": result[0], "nombre": result[1]}

@router.post("/")
async def create_contrato(rol: Rol):
    con.execute("INSERT INTO rol (id, nombre) VALUES (:id, :nombre)", [rol.id, rol.nombre])
    connection.commit()
    return {"message": "Rol creado correctamente"}

@router.put("/{id}")
async def update_contrato(id: int, rol: Rol):
    con.execute("UPDATE rol SET nombre = :nombre WHERE id = :id", {"nombre": rol.nombre, "id": id})
    con.commit()
    return {"message": "Rol actualizado correctamente"}

@router.delete("/{id}")
async def delete_contrato(id: int):
    con.execute("DELETE FROM rol WHERE id = :id", {"id": id})
    con.commit()
    return {"message": "Rol eliminado correctamente"}

