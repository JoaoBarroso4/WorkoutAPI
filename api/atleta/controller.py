from fastapi import APIRouter, status, Body
from api.atleta.schemas import AtletaInSchema
from api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    '/',
    summary='Cadastra um novo atleta',
    status_code=status.HTTP_201_CREATED,
)
async def post(
        db_session: DatabaseDependency,
        atleta_in: AtletaInSchema = Body(...)
):
    pass
