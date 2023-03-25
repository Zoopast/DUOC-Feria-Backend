from fastapi import APIRouter, HTTPException
from db.client import get_cursor
from db.models.user import Usuario
router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "Not found"}},
)

con = get_cursor()

# Rutas para operaciones CRUD
@router.get("/usuario/{id}")
async def obtener_usuario(id: int):
    with con.cursor() as cur:
        cur.execute("SELECT * FROM usuario WHERE id = :id", {"id": id})
        result = cur.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"id": result[0], "nombre": result[1], "rol_id": result[2]}

@router.post("/usuario")
async def crear_usuario(usuario: Usuario):
    with con.cursor() as cur:
        cur.execute("INSERT INTO usuario (id, nombre, rol_id) VALUES (:id, :nombre, :rol_id)", {"id": usuario.id, "nombre": usuario.nombre, "rol_id": usuario.rol_id})
        con.commit()
        return {"message": "Usuario creado correctamente"}

@router.put("/usuario/{id}")
async def actualizar_usuario(id: int, usuario: Usuario):
    with con.cursor() as cur:
        cur.execute("UPDATE usuario SET nombre = :nombre, rol_id = :rol_id WHERE id = :id", {"nombre": usuario.nombre, "rol_id": usuario.rol_id, "id": id})
        con.commit()
        return {"message": "Usuario actualizado correctamente"}

@router.delete("/usuario/{id}")
async def eliminar_usuario(id: int):
    with con.cursor() as cur:
        cur.execute("DELETE FROM usuario WHERE id = :id", {"id": id})
        con.commit()
        return {"message": "Usuario eliminado correctamente"}