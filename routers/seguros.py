from fastapi import APIRouter, HTTPException
from db.client import get_cursor
from db.models.seguro import Seguro

router = APIRouter(
    prefix="/seguros",
    tags=["seguros"],
    responses={404: {"description": "Not found"}},
)

con, connection = get_cursor()

@router.get("/")
async def get_seguros():
    con.execute("SELECT * FROM SEGUROS")
    result = con.fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="Seguro no encontrado")
    return [{"id": row[0], "nombre": row[1]} for row in result]

@router.get("/{id_seguro}")
async def get_seguro(id_seguro: int):
    con.execute("SELECT * FROM SEGUROS WHERE id = :id", {"id": id_seguro})
    result = con.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Seguro no encontrado")
    return {"id": result[0], "nombre": result[1]}

@router.post("/")
async def create_seguro(seguro: Seguro):
    con.execute("INSERT INTO SEGUROS (id, nombre) VALUES (:id, :nombre)", [seguro.id_seguro, seguro.nombre])
    connection.commit()
    return {"message": "Seguro creado correctamente"}

@router.put("/{id_seguro}")
async def update_seguro(id_seguro: int, seguro: Seguro):
    con.execute("UPDATE SEGUROS SET nombre = :nombre WHERE id = :id", {"nombre": seguro.nombre, "id": id_seguro})
    con.commit()
    return {"message": "Seguro actualizado correctamente"}

@router.delete("/{id_seguro}")
async def delete_seguro(id_seguro: int):
    con.execute("DELETE FROM SEGUROS WHERE id = :id", {"id": id_seguro})
    con.commit()
    return {"message": "Seguro eliminado correctamente"}