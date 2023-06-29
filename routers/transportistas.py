from fastapi import APIRouter, HTTPException, status
from db.schemas.user import user_tuple_to_dict
from db.client import get_cursor

router = APIRouter(
    prefix="/transportistas",
    tags=["transportistas"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
  )

con, connection = get_cursor()

@router.get("/")
async def obtener_transportistas():
  try:

    con.execute("SELECT * FROM USUARIOS WHERE rol='Transportista'")
    result = con.fetchall()
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  return [user_tuple_to_dict(user) for user in result]

@router.get("/{id_transportista}")
async def obtener_transportista(id_transportista: int):
  con.execute("SELECT * FROM USUARIOS WHERE id_usuario = :id_transportista", {"id_usuario": id_transportista})
  result = con.fetchone()
  if not result:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transportista no encontrado")

  return user_tuple_to_dict(result)

@router.delete("/{id_transportista}")
async def eliminar_transportista(id_transportista: int):
  con.execute("DELETE FROM USUARIOS WHERE id_usuario = :id_transportista", {"id_usuario": id_transportista})
  connection.commit()
  return { "status": status.HTTP_200_OK, "message": "Transportista eliminado"}
