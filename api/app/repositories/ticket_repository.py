from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.repositories.base import RepositorioBase


class TicketRepository(RepositorioBase[Ticket]):
    def __init__(self, db: Session):
        super().__init__(db, Ticket)
    