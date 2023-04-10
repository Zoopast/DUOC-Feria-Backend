from fastapi import APIRouter, Depends, HTTPException, status
from db.models.comerciante import Comerciante
from db.schemas.comerciante import comerciante_schema
from db.client import get_cursor

router = APIRouter(
    prefix="/comerciantes",
    tags=["comerciantes"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
  )

con, connection = get_cursor()

@router.get("/")
async def obtener_comerciantes():
  con.execute("SELECT * FROM COMERCIANTES")
  result = con.fetchall()
  return result

@router.get("/{id_comerciante}")
async def obtener_comerciante(id_comerciante: int):
  con.execute("SELECT * FROM COMERCIANTES WHERE id_comerciante = :id_comerciante", {"id_comerciante": id_comerciante})
  result = con.fetchone()
  if not result:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comerciante no encontrado")
  
  return comerciante_schema(result)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_comerciante(comerciante: Comerciante):
  print(comerciante)
  con.execute("""
    INSERT INTO COMERCIANTES(nombre, email, telefono, direccion, id_usuario) 
    VALUES (:nombre, :email, :telefono, :direccion, :id_usuario)"""
    , {"nombre": comerciante.nombre, "email": comerciante.email, "telefono": comerciante.telefono, "direccion": comerciante.direccion, "id_usuario": comerciante.id_usuario})
  connection.commit()
  return { "status": status.HTTP_201_CREATED, "message": "Comerciante creado"}

@router.put("/{id_comerciante}")
async def actualizar_comerciante(id_comerciante: int, comerciante: Comerciante):
  con.execute("""
    UPDATE COMERCIANTES SET nombre = :nombre, email = :email, telefono = :telefono, direccion = :direccion, id_usuario = :id_usuario
    WHERE id_comerciante = :id_comerciante
  """, {"id_comerciante": id_comerciante, "nombre": comerciante.nombre, "email": comerciante.email, "telefono": comerciante.telefono, "direccion": comerciante.direccion, "id_usuario": comerciante.id_usuario})
  connection.commit()
  return { "status": status.HTTP_200_OK, "message": "Comerciante actualizado"}

@router.delete("/{id_comerciante}")
async def eliminar_comerciante(id_comerciante: int):
  con.execute("DELETE FROM COMERCIANTES WHERE id_comerciante = :id_comerciante", {"id_comerciante": id_comerciante})
  connection.commit()
  return { "status": status.HTTP_200_OK, "message": "Comerciante eliminado"}
