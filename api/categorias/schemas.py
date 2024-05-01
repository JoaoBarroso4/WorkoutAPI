from pydantic import Field, UUID4
from typing import Annotated

from api.contrib.schemas import BaseSchema


class CategoriaInSchema(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", example="Scale", max_length=10)]

class CategoriaOutSchema(CategoriaInSchema):
    id: Annotated[UUID4, Field(description="ID da categoria")]