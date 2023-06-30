from fastapi import APIRouter, HTTPException, status
from db.schemas.user import user_tuple_to_dict
from db.client import get_cursor

router = APIRouter(
    prefix="/clientes_externos",
    tags=["clientes_externos"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
  )

con, connection = get_cursor()

@router.get("/")
async def obtener_clientes_externoes():
  try:

    con.execute("SELECT * FROM USUARIOS WHERE rol='Cliente externo'")
    result = con.fetchall()
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  return [user_tuple_to_dict(user) for user in result]

@router.get("/{id_clientes_externo}")
async def obtener_clientes_externo(id_clientes_externo: int):
  con.execute("SELECT * FROM USUARIOS WHERE id_usuario = :id_clientes_externo", {"id_usuario": id_clientes_externo})
  result = con.fetchone()
  if not result:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente externo no encontrado")

  return user_tuple_to_dict(result)

@router.delete("/{id_clientes_externo}")
async def eliminar_clientes_externo(id_clientes_externo: int):
  con.execute("DELETE FROM USUARIOS WHERE id_usuario = :id_clientes_externo", {"id_usuario": id_clientes_externo})
  connection.commit()
  return { "status": status.HTTP_200_OK, "message": "clientes_externo eliminado"}
