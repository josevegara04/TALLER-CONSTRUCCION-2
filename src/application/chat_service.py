from datetime import datetime
from typing import List, Optional

from ..domain.repositories import IProductRepository, IChatRepository
from ..domain.entities import ChatMessage, ChatContext, Product
from .dtos import (
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ChatHistoryDTO
)


class ChatService:
    """
    Servicio para gestionar el chat
    """

    def __init__(
        self,
        product_repository: IProductRepository,
        chat_repository: IChatRepository,
        ai_service  # GeminiService
    ):
        """
        Inicializa el servicio de chat
        """

        self.product_repository = product_repository
        self.chat_repository = chat_repository
        self.ai_service = ai_service

    async def process_message(
        self,
        request: ChatMessageRequestDTO
    ) -> ChatMessageResponseDTO:
        """
        Procesa un mensaje del usuario y retorna la respuesta del asistente
        """

        try:
            # 1. Obtener productos
            products: List[Product] = self.product_repository.get_all()

            # 2. Obtener historial reciente (últimos 6)
            history: List[ChatMessage] = self.chat_repository.get_recent_messages(
                request.session_id,
                count=6
            )

            # 3. Crear contexto con tu VO (🔥 bien diseñado)
            context = ChatContext(messages=history)

            # 4. Formatear contexto para IA
            formatted_context = context.format_for_prompt()

            # 5. Llamar a la IA
            ai_response = await self.ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=formatted_context
            )

            # 6. Crear mensaje del usuario
            user_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="user",
                message=request.message,
                timestamp=datetime.utcnow()
            )

            self.chat_repository.save_message(user_msg)

            # 7. Crear mensaje del asistente
            assistant_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="assistant",
                message=ai_response,
                timestamp=datetime.utcnow()
            )

            self.chat_repository.save_message(assistant_msg)

            # 8. Retornar DTO
            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message=ai_response,
                timestamp=datetime.utcnow()
            )

        except Exception as e:
            raise ValueError(f"Error procesando mensaje: {str(e)}")

    # 📜 Historial
    def get_session_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[ChatHistoryDTO]:

        messages = self.chat_repository.get_session_history(session_id, limit)

        return [
            ChatHistoryDTO(
                id=msg.id,
                role=msg.role,
                message=msg.message,
                timestamp=msg.timestamp
            )
            for msg in messages
        ]

    # 🧹 Limpiar historial
    def clear_session_history(self, session_id: str) -> int:
        return self.chat_repository.delete_session_history(session_id)