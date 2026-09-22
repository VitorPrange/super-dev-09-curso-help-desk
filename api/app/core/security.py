import bcrypt


# Gera um salt aleatório e cria o hash seguro da senha usando bcrypt
def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")