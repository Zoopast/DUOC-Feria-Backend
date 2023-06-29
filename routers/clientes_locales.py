from fastapi import APIRouter, HTTPException, status
from db.schemas.user import user_tuple_to_dict
from db.client import get_cursor

router = APIRouter(
    prefix="/clientes_locales",
    tags=["clientes_locales"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
  )

con, connection = get_cursor()

@router.get("/")
async def obtener_clientes_locales():
  try:

    con.execute("SELECT * FROM USUARIOS WHERE rol='Cliente local'")
    result = con.fetchall()
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  return [user_tuple_to_dict(user) for user in result]

@router.get("/{id_clientes_local}")
async def obtener_clientes_local(id_clientes_local: int):
  con.execute("SELECT * FROM USUARIOS WHERE id_usuario = :id_clientes_local", {"id_usuario": id_clientes_local})
  result = con.fetchone()
  if not result:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente local no encontrado")

  return user_tuple_to_dict(result)

@router.delete("/{id_clientes_local}")
async def eliminar_clientes_local(id_clientes_local: int):
  con.execute("DELETE FROM USUARIOS WHERE id_usuario = :id_clientes_local", {"id_usuario": id_clientes_local})
  connection.commit()
  return { "status": status.HTTP_200_OK, "message": "clientes_local eliminado"}
