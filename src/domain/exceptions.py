"""
Excepciones específicas del dominio.
Representan errores de negocio, no errores técnicos.
"""

class ProductNotFoundError(Exception):
    """
    Se lanza cuando se busca un producto que no existe.
    """
    def __init__(self, product_id: Optional[int] = None):
        if product_id:
            super().__init__(f"Producto con ID {product_id} no encontrado")
        else:
            super().__init__("Producto no encontrado")


class InvalidProductDataError(Exception):
    """
    Se lanza cuando los datos de un producto son inválidos.
    """
    def __init__(self, message: Optional[str] = None):
        if message:
            super().__init__(message)
        else:
            super().__init__("Datos de producto inválidos")


class ChatServiceError(Exception):
    """
    Se lanza cuando hay un error en el servicio de chat.
    """
    def __init__(self, message: Optional[str] = None):
        if message:
            super().__init__(message)
        else:
            super().__init__("Error en el servicio de chat")