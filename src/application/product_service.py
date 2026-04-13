from src.domain.repository import IProductRepository
from src.domain.entities import Product
from src.application.dtos import ProductDTO
from typing import List, Dict

class ProductService:
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    def get_all_products(self) -> List[Product]:
        """Obtiene todos los productos"""
        return self.product_repository.get_all()

    def get_product_by_id(self, product_id: int) -> Product:
        """Obtiene un producto por ID"""
        product = self.product_repository.get_by_id(product_id)
        if product is None:
            raise ValueError(f"Producto con ID {product_id} no encontrado")
        return product
    
    def search_product(self, filters: Dict) -> List[Product]:
        products = self.product_repository.get_all()

        if not filters:
            return products
        if "brand" in filters:
            products = [p for p in products if p.brand == filters["brand"]]
            
        if "category" in filters:
            products = [p for p in products if p.category == filters["category"]]

        if "available" in filters:
            products = [p for p in products if p.stock > 0]

        return products

    def create_product(self, product_dto: ProductDTO) -> Product:
        product = Product(
            id=None,
            name=product_dto.name,
            brand=product_dto.brand,
            category=product_dto.category,
            size=product_dto.size,
            color=product_dto.color,
            price=product_dto.price,
            stock=product_dto.stock,
            description=product_dto.description
        )

        return self.product_repository.save(product)

    def update_product(self, product_id: int, product_dto: ProductDTO) -> Product:
        existing_product = self.product_repository.get_by_id(product_id)

        if not existing_product:
            raise ValueError(f"Producto con id {product_id} no existe")

        # actualizar campos
        existing_product.name = product_dto.name
        existing_product.brand = product_dto.brand
        existing_product.category = product_dto.category
        existing_product.size = product_dto.size
        existing_product.color = product_dto.color
        existing_product.price = product_dto.price
        existing_product.stock = product_dto.stock
        existing_product.description = product_dto.description

        return self.product_repository.save(existing_product)

    def delete_product(self, product_id: int) -> bool:
        """Elimina un producto por ID"""

        exists = self.product_repository.get_by_id(product_id)

        if not exists:
            raise ValueError(f"Producto con id {product_id} no existe")

        return self.product_repository.delete(product_id)

    def get_available_products(self) -> List[Product]:
        """Obtiene productos disponibles"""

        products = self.product_repository.get_all()
        return [p for p in products if p.stock > 0]