from uuid import uuid4
from fastapi import APIRouter, status, Body, HTTPException
from pydantic import UUID4
from sqlalchemy.future import select
from api.centro_treinamento.models import CentroTreinamentoModel
from api.centro_treinamento.schemas import CentroTreinamentoInSchema, CentroTreinamentoOutSchema
from api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    '/',
    summary='Cadastra um novo centro de treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOutSchema,
)
async def post(
        db_session: DatabaseDependency,
        centro_treinamento_in: CentroTreinamentoInSchema = Body(...)
) -> CentroTreinamentoOutSchema:
    centro_treinamento_out = CentroTreinamentoOutSchema(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

    db_session.add(centro_treinamento_model)
    await db_session.commit()

    return centro_treinamento_out


@router.get(
    '/',
    summary='Lista todas as categorias',
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOutSchema],
)
async def get_all(
        db_session: DatabaseDependency
) -> list[CentroTreinamentoOutSchema]:
    categorias: list[CentroTreinamentoOutSchema] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()

    return categorias


@router.get(
    '/{id}',
    summary='Busca uma categoria pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOutSchema,
)
async def get_by_id(
        db_session: DatabaseDependency,
        id: UUID4
) -> CentroTreinamentoOutSchema:
    categoria: CentroTreinamentoOutSchema = (await db_session.execute(select(CentroTreinamentoModel).filter_by(pk_id=id))).scalars().first()

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Centro de treinamento não encontrado.')

    return categoria
