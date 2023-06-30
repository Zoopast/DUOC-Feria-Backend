from fastapi import APIRouter, HTTPException, status
from db.schemas.user import user_tuple_to_dict
from db.client import get_cursor

router = APIRouter(
    prefix="/consultores",
    tags=["consultores"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
  )

con, connection = get_cursor()

@router.get("/")
async def obtener_consultores():
  try:

    con.execute("SELECT * FROM USUARIOS WHERE rol='Consultor'")
    result = con.fetchall()
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  return [user_tuple_to_dict(user) for user in result]

@router.get("/{id_consultor}")
async def obtener_consultor(id_consultor: int):
  con.execute("SELECT * FROM USUARIOS WHERE id_usuario = :id_consultor", {"id_usuario": id_consultor})
  result = con.fetchone()
  if not result:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente local no encontrado")

  return user_tuple_to_dict(result)

@router.delete("/{id_consultor}")
async def eliminar_consultor(id_consultor: int):
  con.execute("DELETE FROM USUARIOS WHERE id_usuario = :id_consultor", {"id_usuario": id_consultor})
  connection.commit()
  return { "status": status.HTTP_200_OK, "message": "consultor eliminado"}
