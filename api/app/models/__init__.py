"""
Pacote de models. Importar `app.models` registra as tabelas em Base.metadata
o que o Alembic precisa para gerar as migrations.
"""
from app.core.database import Base
from app.models.categoria import Categoria
from app.core.enums import Papel
from app.models.usuario import Usuario
from app.models.ticket import Ticket


__all__ = ["Base", "Categoria", "Papel", "Usuario", "Ticket"]
