from datetime import datetime, timezone

# Utilitário de data e hora. Guardamos no banco de dados em UTC, sem timezone.
def agora() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)