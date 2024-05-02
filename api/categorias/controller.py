from uuid import uuid4
from fastapi import APIRouter, status, Body, HTTPException
from pydantic import UUID4
from sqlalchemy.future import select
from api.categorias.models import CategoriaModel
from api.categorias.schemas import CategoriaInSchema, CategoriaOutSchema
from api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    '/',
    summary='Cadastra uma nova categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOutSchema,
)
async def post(
        db_session: DatabaseDependency,
        categoria_in: CategoriaInSchema = Body(...)
) -> CategoriaOutSchema:
    categoria_out = CategoriaOutSchema(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())

    db_session.add(categoria_model)
    await db_session.commit()

    return categoria_out


@router.get(
    '/',
    summary='Lista todas as categorias',
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOutSchema],
)
async def get_all(
        db_session: DatabaseDependency
) -> list[CategoriaOutSchema]:
    categorias: list[CategoriaOutSchema] = (await db_session.execute(select(CategoriaModel))).scalars().all()

    return categorias


@router.get(
    '/{id}',
    summary='Busca uma categoria pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOutSchema,
)
async def get_by_id(
        db_session: DatabaseDependency,
        id: UUID4
) -> CategoriaOutSchema:
    categoria: CategoriaOutSchema = (await db_session.execute(select(CategoriaModel).filter_by(pk_id=id))).scalars().first()

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não encontrada.')

    return categoria
