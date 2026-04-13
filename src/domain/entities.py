from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Product:
    """
    Entidad que representa un producto en el e-commerce.
    Contiene la lógica de negocio relacionada con productos.
    """
    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str
    
    def __post_init__(self):
        """
        Validaciones que se ejecutan después de crear el objeto.
        """
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        if not self.name:
            raise ValueError("El nombre no puede estar vacío")
    
    def is_available(self) -> bool:
        """
        Función que verifica que el stock no esté vacío
        """
        return self.stock > 0
    
    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if self.stock < quantity:
            raise ValueError("No hay suficiente stock")
        self.stock -= quantity
    
    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        self.stock += quantity

@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en el chat.
    """
    id: Optional[int]
    session_id: str
    role: str  # 'user' o 'assistant'
    message: str
    timestamp: datetime
    
    def __post_init__(self):
        """
        Validaciones al crear el objecto
        """
        if self.role not in ['user', 'assistant']:
            raise ValueError("El rol debe ser 'user' o 'assistant'")
        if not self.message:
            raise ValueError("El mensaje no puede estar vacío")
        if not self.session_id:
            raise ValueError("La sesión no puede estar vacía")
    
    def is_from_user(self) -> bool:
        """
        Verifica que sea un mensaje del usuario
        """
        return self.role == 'user'
    
    def is_from_assistant(self) -> bool:
        """
        Verifica que sea un mensaje del asistente
        """
        return self.role == "assistant"

@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación.
    Mantiene los mensajes recientes para dar coherencia al chat.
    """
    messages: list[ChatMessage]
    max_messages: int = 6
    
    def get_recent_messages(self) -> list[ChatMessage]:
        """
        Retorna los últimos N mensajes (max_messages)
        """
        return self.messages[-self.max_messages:]
    
    def format_for_prompt(self) -> str:
        """
        Formatea los mensajes para incluirlos en el prompt de IA
        """
        formatted_messages = []
        for msg in self.get_recent_messages():
            role_label = "Usuario" if msg.is_from_user() else "Asistente"
            formatted_messages.append(f"{role_label}: {msg.message}")
        return "\n".join(formatted_messages)