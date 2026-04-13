from typing import List, Optional
from sqlalchemy.orm import Session

from ..domain.repositories import IChatRepository
from ..domain.entities import ChatMessage
from ..infrastructure.db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):

    def __init__(self, db: Session):
        """
        Inicializa el repositorio de chat.  
        """

        self.db = db

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        """
        Convierte un modelo de base de datos a una entidad.
        """
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp
        )

    def _entity_to_model(self, entity: ChatMessage) -> ChatMemoryModel:
        """
        Convierte una entidad a un modelo de base de datos.
        """

        return ChatMemoryModel(
            id=entity.id,
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp
        )

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en la base de datos.
        """

        model = self._entity_to_model(message)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return self._model_to_entity(model)

    def get_session_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Obtiene el historial de mensajes de una sesión.
        """

        query = self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).order_by(ChatMemoryModel.timestamp.asc())

        if limit:
            query = query.limit(limit)

        models = query.all()

        return [self._model_to_entity(m) for m in models]

    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina el historial de mensajes de una sesión.
        """

        query = self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        )

        count = query.count()

        query.delete()
        self.db.commit()

        return count

    def get_recent_messages(
        self,
        session_id: str,
        count: int
    ) -> List[ChatMessage]:
        """
        Obtiene los mensajes más recientes de una sesión.
        """

        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())  # 🔥 más recientes primero
            .limit(count)
            .all()
        )

        models.reverse()

        return [self._model_to_entity(m) for m in models]