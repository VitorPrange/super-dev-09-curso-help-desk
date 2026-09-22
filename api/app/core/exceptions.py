# ErroAplicacao é uma classe que herda Exception
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ErroAplicacao(Exception):
    status_code = 500
    codigo = "erro_interno"

    def __init__(self, mensagem: str, detalhes: list | None = None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.detalhes = detalhes or []


class NaoEncontradoError(ErroAplicacao):
    status_code = 404
    codigo = "nao_encontrado"


class ConflitoError(ErroAplicacao):
    status_code = 409
    codigo = "conflito"


class PermissaoNegadaError(ErroAplicacao):
    status_code = 403
    codigo = "permissao_negada"


class RegraNegocioError(ErroAplicacao):
    status_code = 422
    codigo = "regra_negocio"


def __corpo_erro(codigo: str, mensagem: str, detalhes: list) -> dict:
    return {"codigo": codigo, "mensagem": mensagem, "detalhes": detalhes}

def registrar_handler(app: FastAPI) -> None:
    @app.exception_handler(ErroAplicacao)
    async def tratar_erro_aplicacao(request: Request, exception: ErroAplicacao):
        return JSONResponse(
            status_code=exception.status_code,
            content=__corpo_erro(
                exception.codigo,
                exception.mensagem,
                exception.detalhes
            )
        )
