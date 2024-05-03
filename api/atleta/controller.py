from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, status, Body, HTTPException
from pydantic import UUID4
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api import CategoriaModel, CentroTreinamentoModel
from api.atleta.schemas import AtletaInSchema, AtletaOutSchema, AtletaUpdateSchema
from api.atleta.models import AtletaModel
from api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    '/',
    summary='Cadastra um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOutSchema,
)
async def post(
        db_session: DatabaseDependency,
        atleta_in: AtletaInSchema = Body(...)
):
    nome_categoria = atleta_in.categoria.nome
    nome_centro_treinamento = atleta_in.centro_treinamento.nome

    result_categoria = await db_session.execute(
        select(CategoriaModel)
        .filter_by(nome=nome_categoria)
    )
    categoria = result_categoria.scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Categoria {nome_categoria} não encontrada.'
        )

    result_centro_treinamento = await db_session.execute(
        select(CentroTreinamentoModel)
        .filter_by(nome=nome_centro_treinamento)
    )
    centro_treinamento = result_centro_treinamento.scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Centro de treinamento {nome_centro_treinamento} não encontrado.'
        )

    try:
        atleta_out = AtletaOutSchema(id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump())
        atleta_out_dict = atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'})
        atleta_model = AtletaModel(**atleta_out_dict)

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao cadastrar o atleta.'
        )
    return atleta_out


@router.get(
    '/',
    summary='Lista todos os atletas',
    response_model=list[AtletaOutSchema],
)
async def get(db_session: DatabaseDependency) -> list[AtletaOutSchema]:
    result_atletas = await db_session.execute(
        select(AtletaModel).options(
            selectinload(AtletaModel.categoria),
            selectinload(AtletaModel.centro_treinamento)
        ))
    atletas: list[AtletaOutSchema] = result_atletas.scalars().all()

    return [AtletaOutSchema.model_validate(atleta) for atleta in atletas]


@router.get(
    '/{id}',
    summary='Busca um atleta pelo ID',
    response_model=AtletaOutSchema,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOutSchema:
    atleta: AtletaOutSchema = await db_session.execute(
        select(AtletaModel)
        .filter_by(id=id)
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta {id} não encontrado.'
        )

    return atleta


@router.patch(
    '/{id}',
    summary='Atualiza um cadastro de atleta pelo ID',
    response_model=AtletaOutSchema,
)
async def patch(
        id: UUID4,
        db_session: DatabaseDependency,
        atleta_up: AtletaUpdateSchema = Body(...)
) -> AtletaOutSchema:
    result_atleta = await db_session.execute(
        select(AtletaModel)
        .options(
            selectinload(AtletaModel.categoria),
            selectinload(AtletaModel.centro_treinamento)
        )
        .filter_by(id=id)
    )
    atleta: AtletaOutSchema = result_atleta.scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta {id} não encontrado.'
        )

    update_data = atleta_up.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key in ['categoria', 'centro_treinamento']:
            Model = CategoriaModel if key == 'categoria' else CentroTreinamentoModel
            try:
                result = await db_session.execute(
                    select(Model)
                    .filter_by(nome=value['nome'])
                )
                instance = result.scalars().first()
                setattr(atleta, key, instance)
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{key.capitalize()} '{value['nome']}' não encontrado."
                )
        elif hasattr(atleta, key):
            setattr(atleta, key, value)

    try:
        await db_session.commit()
        await db_session.refresh(atleta)
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    return atleta


@router.delete(
    '/{id}',
    summary='Remove um atleta pelo ID',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    result_atleta = await db_session.execute(
        select(AtletaModel)
        .filter_by(id=id)
    )
    atleta = result_atleta.scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta {id} não encontrado.'
        )

    await db_session.delete(atleta)
    await db_session.commit()
