from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Index
from datetime import datetime

from src.infrastructure.db.database import Base


class ProductModel(Base):
    """
    Modelo ORM para la tabla 'products'.
    Representa cómo se almacenan los productos en la base de datos.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(100))
    category = Column(String(100))
    size = Column(String(20))
    color = Column(String(50))
    price = Column(Float)
    stock = Column(Integer)
    description = Column(Text)

    # Índices para búsquedas frecuentes
    __table_args__ = (
        Index("idx_product_brand", "brand"),
        Index("idx_product_category", "category"),
    )


class ChatMemoryModel(Base):
    """
    Modelo ORM para la tabla 'chat_memory'.
    Guarda el historial de conversaciones del chat.
    """
    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), index=True)
    role = Column(String(20))  # 'user' o 'assistant'
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Índice compuesto (muy útil para queries de historial)
    __table_args__ = (
        Index("idx_session_timestamp", "session_id", "timestamp"),
    )