from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.contrib.models import BaseModel


class AtletaModel(BaseModel):
    __tablename__ = "atletas"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), nullable=False, unique=True)
    data_nascimento: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    categoria: Mapped['CategoriaModel'] = relationship(back_populates="atletas")
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.pk_id"), nullable=False)

    centro_treinamento: Mapped['CentroTreinamentoModel'] = relationship(back_populates="atletas")
    centro_treinamento_id: Mapped[int] = mapped_column(ForeignKey("centros_treinamento.pk_id"), nullable=False)