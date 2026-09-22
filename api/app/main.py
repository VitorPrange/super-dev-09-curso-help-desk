from fastapi import FastAPI
from app.core.exceptions import registrar_handler
from app.controllers.usuario_controller import router as usuario_router
from app.controllers.categoria_controller import router as categoria_router
from app.controllers.ticket_controller import router as ticket_router


app = FastAPI()

# Traduz as exceções de domínio (app/core/exceptions.py) para respostas HTTP padronizadas
registrar_handler(app)

app.include_router(categoria_router)
app.include_router(usuario_router)
app.include_router(ticket_router)

# Executar
# uvicorn app.main:app --reload
# Chrome: localhost:8000/docs