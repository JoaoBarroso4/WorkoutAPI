from datetime import date
from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from api.categorias.schemas import CategoriaInSchema
from api.centro_treinamento.schemas import CentroTreinamentoInSchema
from api.contrib.schemas import BaseSchema, OutMixin


class AtletaSchema(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="João", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="123.456.789-00", max_length=14)]
    data_nascimento: Annotated[date, Field(description="Data de nascimento do atleta", example="2000-01-01", format="date")]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example=70.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example=1.75)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", max_length=1)]
    categoria: Annotated[CategoriaInSchema, Field(description="Categoria do atleta")]
    centro_treinamento: Annotated[CentroTreinamentoInSchema, Field(description="Centro de treinamento do atleta")]


class AtletaInSchema(AtletaSchema):
    pass


class AtletaOutSchema(AtletaSchema, OutMixin):
    pass

class AtletaUpdateSchema(AtletaSchema):
    nome: Annotated[Optional[str], Field(description="Nome do atleta", example="João", max_length=50)]
    data_nascimento: Annotated[Optional[date], Field(description="Data de nascimento do atleta", example="2000-01-01", format="date")]