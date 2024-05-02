from pydantic import Field, UUID4
from typing import Annotated
from api.contrib.schemas import BaseSchema


class CentroTreinamentoSchema(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="CT Fit", max_length=20)]
    endereco: Annotated[str, Field(description="Endereço do centro de treinamento", example="Rua 1, 123", max_length=60)]
    proprietario: Annotated[str, Field(description="Proprietário do centro de treinamento", example="João da Silva", max_length=30)]


class CentroTreinamentoInSchema(CentroTreinamentoSchema):
    pass


class CentroTreinamentoOutSchema(CentroTreinamentoSchema):
    id: Annotated[UUID4, Field(description="ID do centro de treinamento")]