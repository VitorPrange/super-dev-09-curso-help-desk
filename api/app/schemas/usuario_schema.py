from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enums import Papel


class UsuarioCriar(BaseModel):
    nome: str = Field(min_length=2, max_length=120, description="Nome completo")
    email: EmailStr = Field(description="E-mail único no sistema")
    senha: str = Field(min_length=6, max_length=72, description="Senha entre 6 e 72 caracteres")
    papel: Papel = Field(description="Papel do usuário: ADMIN, ATENDENTE ou SOLICITANTE")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "Ana Souza",
                "email": "ana@helpdesk.com",
                "senha": "Atende@123",
                "papel": "ATENDENTE",
            }
        }
    )


class UsuarioListar(BaseModel):
    id: int = Field()
    nome: str = Field()
    email: EmailStr = Field()
    papel: str = Field(description="ADMIN, ATENDETE ou SOLICITANTE")

    model_config = ConfigDict(from_attributes=True)


class UsuarioEditar(BaseModel):
    nome: str = Field(min_length=2, max_length=120, description="Nome completo")
    email: EmailStr = Field(description="E-mail único no sistema")
    senha: str = Field(min_length=6, max_length=72, description="Senha entre 6 e 72 caracteres")
    papel: Papel = Field(description="Papel do usuário: ADMIN, ATENDENTE ou SOLICITANTE")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "Ana Souza",
                "email": "ana@helpdesk.com",
                "senha": "Atende@123",
                "papel": "ATENDENTE",
            }
        }
    )