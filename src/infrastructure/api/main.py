from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from src.infrastructure.db.database import get_db, init_db
from src.infrastructure.repositories.product_repository import SQLProductRepository
from src.infrastructure.repositories.chat_repository import SQLChatRepository
from src.infrastructure.llm_providers.gemini_service import GeminiService

from src.application.product_service import ProductService
from src.application.chat_service import ChatService

from src.application.dtos import (
    ProductDTO,
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ChatHistoryDTO
)

app = FastAPI(
    title="E-commerce Chat API",
    description="API con IA para recomendación de productos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    # Inicializa la base de datos
    init_db()


@app.get("/")
def root():
    # Endpoint raíz

    return {
        "name": "E-commerce Chat API",
        "version": "1.0.0",
        "endpoints": [
            "/products",
            "/products/{id}",
            "/chat",
            "/chat/history/{session_id}",
            "/health"
        ]
    }


@app.get("/products", response_model=List[ProductDTO])
def get_products(db: Session = Depends(get_db)):
    # Endpoint para obtener todos los productos

    try:
        repo = SQLProductRepository(db)
        service = ProductService(repo)

        products = service.get_all_products()
        return products

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products/{product_id}", response_model=ProductDTO)
def get_product(product_id: int, db: Session = Depends(get_db)):
    # Endpoint para obtener un producto por ID

    try:
        repo = SQLProductRepository(db)
        service = ProductService(repo)

        product = service.get_product_by_id(product_id)
        return product

    except ValueError:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatMessageResponseDTO)
async def chat(
    request: ChatMessageRequestDTO,
    db: Session = Depends(get_db)
):
    # Endpoint para chatear con la IA

    try:
        product_repo = SQLProductRepository(db)
        chat_repo = SQLChatRepository(db)
        ai_service = GeminiService()

        service = ChatService(product_repo, chat_repo, ai_service)

        response = await service.process_message(request)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/history/{session_id}", response_model=List[ChatHistoryDTO])
def get_chat_history(
    session_id: str,
    limit: Optional[int] = 10,
    db: Session = Depends(get_db)
):
    # Endpoint para obtener el historial de chat

    try:
        product_repo = SQLProductRepository(db)
        chat_repo = SQLChatRepository(db)
        ai_service = GeminiService()

        service = ChatService(product_repo, chat_repo, ai_service)

        history = service.get_session_history(session_id, limit)
        return history

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/chat/history/{session_id}")
def delete_chat_history(
    session_id: str,
    db: Session = Depends(get_db)
):
    # Endpoint para eliminar el historial de chat

    try:
        product_repo = SQLProductRepository(db)
        chat_repo = SQLChatRepository(db)
        ai_service = GeminiService()

        service = ChatService(product_repo, chat_repo, ai_service)

        deleted_count = service.clear_session_history(session_id)

        return {
            "message": "Historial eliminado",
            "deleted_messages": deleted_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    # Endpoint para verificar el estado de la API
    
    return {
        "status": "ok",
        "timestamp": datetime.utcnow()
    }