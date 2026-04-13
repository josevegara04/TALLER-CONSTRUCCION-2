import pytest
from datetime import datetime

from src.domain.entities import Product, ChatMessage, ChatContext


# 🧪 -------- Product Tests --------

def test_product_valid_creation():
    product = Product(
        id=1,
        name="Nike Air",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=100.0,
        stock=10,
        description="Zapatilla"
    )

    assert product.name == "Nike Air"
    assert product.price == 100.0


def test_product_invalid_price():
    with pytest.raises(ValueError):
        Product(
            id=1,
            name="Test",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=0,
            stock=10,
            description="Test"
        )


def test_product_invalid_stock():
    with pytest.raises(ValueError):
        Product(
            id=1,
            name="Test",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=100,
            stock=-1,
            description="Test"
        )


def test_product_is_available():
    product = Product(
        id=1,
        name="Test",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=100,
        stock=5,
        description="Test"
    )

    assert product.is_available() is True


def test_product_reduce_stock():
    product = Product(
        id=1,
        name="Test",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=100,
        stock=10,
        description="Test"
    )

    product.reduce_stock(3)
    assert product.stock == 7


def test_product_reduce_stock_error():
    product = Product(
        id=1,
        name="Test",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=100,
        stock=2,
        description="Test"
    )

    with pytest.raises(ValueError):
        product.reduce_stock(5)


# 🧪 -------- ChatMessage Tests --------

def test_chat_message_valid():
    msg = ChatMessage(
        id=1,
        session_id="abc123",
        role="user",
        message="Hola",
        timestamp=datetime.utcnow()
    )

    assert msg.is_from_user() is True


def test_chat_message_invalid_role():
    with pytest.raises(ValueError):
        ChatMessage(
            id=1,
            session_id="abc123",
            role="invalid",
            message="Hola",
            timestamp=datetime.utcnow()
        )


def test_chat_message_empty_message():
    with pytest.raises(ValueError):
        ChatMessage(
            id=1,
            session_id="abc123",
            role="user",
            message="",
            timestamp=datetime.utcnow()
        )


# 🧪 -------- ChatContext Tests --------

def test_chat_context_recent_messages():
    messages = [
        ChatMessage(
            id=i,
            session_id="s1",
            role="user",
            message=f"msg {i}",
            timestamp=datetime.utcnow()
        )
        for i in range(10)
    ]

    context = ChatContext(messages=messages, max_messages=5)

    recent = context.get_recent_messages()

    assert len(recent) == 5
    assert recent[0].message == "msg 5"


def test_chat_context_format_for_prompt():
    messages = [
        ChatMessage(
            id=1,
            session_id="s1",
            role="user",
            message="Hola",
            timestamp=datetime.utcnow()
        ),
        ChatMessage(
            id=2,
            session_id="s1",
            role="assistant",
            message="Hola, ¿en qué puedo ayudarte?",
            timestamp=datetime.utcnow()
        ),
    ]

    context = ChatContext(messages=messages)

    formatted = context.format_for_prompt()

    assert "Usuario: Hola" in formatted
    assert "Asistente: Hola, ¿en qué puedo ayudarte?" in formatted