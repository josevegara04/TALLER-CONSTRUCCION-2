import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock

from src.application.product_service import ProductService
from src.application.chat_service import ChatService

from src.domain.entities import Product, ChatMessage
from src.application.dtos import ProductDTO, ChatMessageRequestDTO


# 🧪 ---------- FIXTURES ----------

@pytest.fixture
def mock_product_repo():
    return Mock()


@pytest.fixture
def mock_chat_repo():
    return Mock()


@pytest.fixture
def mock_ai_service():
    mock = Mock()
    mock.generate_response = AsyncMock(return_value="Respuesta IA")
    return mock


# 🧪 ---------- ProductService ----------

def test_get_all_products(mock_product_repo):
    mock_product_repo.get_all.return_value = [
        Product(1, "Nike", "Nike", "Running", "42", "Negro", 100, 10, "Test")
    ]

    service = ProductService(mock_product_repo)

    result = service.get_all_products()

    assert len(result) == 1
    assert result[0].name == "Nike"


def test_get_product_by_id_not_found(mock_product_repo):
    mock_product_repo.get_by_id.return_value = None

    service = ProductService(mock_product_repo)

    with pytest.raises(ValueError):
        service.get_product_by_id(1)


def test_create_product(mock_product_repo):
    dto = ProductDTO(
        name="Adidas",
        brand="Adidas",
        category="Running",
        size="42",
        color="Blanco",
        price=120,
        stock=5,
        description="Test"
    )

    mock_product_repo.save.return_value = Product(
        1, dto.name, dto.brand, dto.category,
        dto.size, dto.color, dto.price, dto.stock, dto.description
    )

    service = ProductService(mock_product_repo)

    result = service.create_product(dto)

    assert result.name == "Adidas"
    assert result.id == 1


def test_delete_product_not_found(mock_product_repo):
    mock_product_repo.get_by_id.return_value = None

    service = ProductService(mock_product_repo)

    with pytest.raises(ValueError):
        service.delete_product(1)


# 🧪 ---------- ChatService ----------

@pytest.mark.asyncio
async def test_process_message(mock_product_repo, mock_chat_repo, mock_ai_service):

    mock_product_repo.get_all.return_value = [
        Product(1, "Nike", "Nike", "Running", "42", "Negro", 100, 10, "Test")
    ]

    mock_chat_repo.get_recent_messages.return_value = []

    request = ChatMessageRequestDTO(
        session_id="s1",
        message="Hola"
    )

    service = ChatService(
        mock_product_repo,
        mock_chat_repo,
        mock_ai_service
    )

    response = await service.process_message(request)

    assert response.session_id == "s1"
    assert response.assistant_message == "Respuesta IA"


@pytest.mark.asyncio
async def test_process_message_handles_exception(
    mock_product_repo,
    mock_chat_repo,
    mock_ai_service
):
    mock_product_repo.get_all.side_effect = Exception("DB error")

    request = ChatMessageRequestDTO(
        session_id="s1",
        message="Hola"
    )

    service = ChatService(
        mock_product_repo,
        mock_chat_repo,
        mock_ai_service
    )

    with pytest.raises(ValueError):
        await service.process_message(request)


def test_get_session_history(mock_product_repo, mock_chat_repo, mock_ai_service):
    mock_chat_repo.get_session_history.return_value = [
        ChatMessage(
            id=1,
            session_id="s1",
            role="user",
            message="Hola",
            timestamp=datetime.utcnow()
        )
    ]

    service = ChatService(
        mock_product_repo,
        mock_chat_repo,
        mock_ai_service
    )

    history = service.get_session_history("s1")

    assert len(history) == 1
    assert history[0].message == "Hola"


def test_clear_session_history(mock_product_repo, mock_chat_repo, mock_ai_service):
    mock_chat_repo.delete_session_history.return_value = 3

    service = ChatService(
        mock_product_repo,
        mock_chat_repo,
        mock_ai_service
    )

    result = service.clear_session_history("s1")

    assert result == 3