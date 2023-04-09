from fastapi import APIRouter, Depends, HTTPException, status
from db.models.productor import Productor
from db.schemas.productor import productor_schema
from db.client import get_cursor

router = APIRouter(
    prefix="/productores",
    tags=["productores"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
  )

con, connection = get_cursor()

@router.get("/")
async def obtener_productores():
  con.execute("SELECT * FROM PRODUCTORES")
  result = con.fetchall()
  return result

@router.get("/{id_productor}")
async def obtener_productor(id_productor: int):
  con.execute("SELECT * FROM PRODUCTORES WHERE id_productor = :id_productor", {"id_productor": id_productor})
  result = con.fetchone()
  if not result:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Productor no encontrado")
  
  return productor_schema(result)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_productor(productor: Productor):
  print(productor)
  con.execute("""
    INSERT INTO PRODUCTORES(nombre, email, telefono, direccion, id_usuario) 
    VALUES (:nombre, :email, :telefono, :direccion, :id_usuario)"""
    , {"nombre": productor.nombre, "email": productor.email, "telefono": productor.telefono, "direccion": productor.direccion, "id_usuario": productor.id_usuario})
  connection.commit()
  return { "status": status.HTTP_201_CREATED, "message": "Productor creado"}