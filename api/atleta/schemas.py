from datetime import date
from typing import Annotated
from pydantic import Field, PositiveFloat
from api.contrib.schemas import BaseSchema, OutMixin


class AtletaSchema(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="João", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="123.456.789-00", max_length=14)]
    data_nascimento: Annotated[date, Field(description="Data de nascimento do atleta", example="01/01/2000", format="date")]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example=70.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example=1.75)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", max_length=1)]


class AtletaInSchema(AtletaSchema):
    pass


class AtletaOutSchema(AtletaSchema, OutMixin):
    pass
