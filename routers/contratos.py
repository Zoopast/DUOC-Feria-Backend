from fastapi import APIRouter, Depends, HTTPException, status
from db.client import get_cursor
from db.schemas.contratos import contrato_tuple_to_dict

con, connection = get_cursor()

router = APIRouter(
    prefix="/contratos",
    tags=["contratos"],
    # dependencies=[Depends(get_token_header)],
		responses={404: {"description": "Not found"}},
)

@router.get("/")
def get_contratos():
	try:
		con.execute("SELECT * FROM CONTRATOS")
		result = con.fetchall()
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
	return [contrato_tuple_to_dict(contrato) for contrato in result]