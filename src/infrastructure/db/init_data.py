from sqlalchemy.orm import Session
from src.infrastructure.db.models import ProductModel

def load_initial_data(db: Session):
    """
    Carga datos iniciales en la base de datos
    """
    
    count = db.query(ProductModel).count()

    if count > 0:
        print("Datos ya existentes. No se cargaran datos iniciales")
        return 

    products = [
        ProductModel(
            name="Nike Air Zoom Pegasus",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120.0,
            stock=10,
            description="Zapatillas cómodas para running diario"
        ),
        ProductModel(
            name="Adidas Ultraboost",
            brand="Adidas",
            category="Running",
            size="41",
            color="Blanco",
            price=180.0,
            stock=8,
            description="Alta amortiguación y retorno de energía"
        ),
        ProductModel(
            name="Puma RS-X",
            brand="Puma",
            category="Casual",
            size="43",
            color="Azul",
            price=95.0,
            stock=15,
            description="Estilo urbano moderno"
        ),
        ProductModel(
            name="Nike Air Force 1",
            brand="Nike",
            category="Casual",
            size="42",
            color="Blanco",
            price=110.0,
            stock=20,
            description="Clásico atemporal"
        ),
        ProductModel(
            name="Adidas Stan Smith",
            brand="Adidas",
            category="Casual",
            size="40",
            color="Verde",
            price=85.0,
            stock=12,
            description="Diseño minimalista"
        ),
        ProductModel(
            name="Puma Smash V2",
            brand="Puma",
            category="Casual",
            size="41",
            color="Negro",
            price=70.0,
            stock=18,
            description="Estilo sencillo y elegante"
        ),
        ProductModel(
            name="Nike Revolution 6",
            brand="Nike",
            category="Running",
            size="44",
            color="Gris",
            price=65.0,
            stock=25,
            description="Ligereza y comodidad"
        ),
        ProductModel(
            name="Adidas Runfalcon",
            brand="Adidas",
            category="Running",
            size="42",
            color="Negro",
            price=60.0,
            stock=30,
            description="Perfectas para principiantes"
        ),
        ProductModel(
            name="Zapato Formal Clásico",
            brand="Clarks",
            category="Formal",
            size="42",
            color="Marrón",
            price=150.0,
            stock=5,
            description="Elegante para ocasiones formales"
        ),
        ProductModel(
            name="Zapato Formal Premium",
            brand="Hugo Boss",
            category="Formal",
            size="43",
            color="Negro",
            price=200.0,
            stock=3,
            description="Alta calidad y diseño exclusivo"
        ),
    ]

    db.add_all(products)
    
    db.commit()

    print("Datos iniciales cargados correctamente")