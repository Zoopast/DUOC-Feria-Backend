from fastapi import APIRouter, HTTPException, status
from db.schemas.user import user_tuple_to_dict
from db.client import get_cursor

router = APIRouter(
    prefix="/productores",
    tags=["productores"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
  )

con, connection = get_cursor()

@router.get("/")
async def obtener_productores():
  try:

    con.execute("SELECT * FROM USUARIOS WHERE rol='Productor'")
    result = con.fetchall()
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  return [user_tuple_to_dict(user) for user in result]

@router.get("/{id_productor}")
async def obtener_productor(id_productor: int):
  con.execute("SELECT * FROM USUARIOS WHERE id_usuario = :id_productor", {"id_usuario": id_productor})
  result = con.fetchone()
  if not result:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Productor no encontrado")

  return user_tuple_to_dict(result)

@router.delete("/{id_productor}")
async def eliminar_productor(id_productor: int):
  con.execute("DELETE FROM USUARIOS WHERE id_usuario = :id_productor", {"id_usuario": id_productor})
  connection.commit()
  return { "status": status.HTTP_200_OK, "message": "Productor eliminado"}
