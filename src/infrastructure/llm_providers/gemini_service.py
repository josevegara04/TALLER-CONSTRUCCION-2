import os
import google.generativeai as genai
from typing import List

from ..domain.entities import Product

class GeminiService:
    """
    Clase que permite la interacción con la API de Gemini.
    """

    def __init__(self):
        """
        Inicializa el servicio de Gemini.
        """

        api_key= os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("No se encontró la API Key de Gemini")

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def format_products_info(self, products: List[Product]) -> str:
        """
        Formatea la información de los productos para que sea entendible por Gemini.
        """
        
        if not products:
            return "No hay productos disponibles."

        formatted = []
        for p in products:
            formatted.append(
                f"- {p.name} | {p.brand} | {p.price} | {p.stock} | {p.category}"
            )

        return "\n".join(formatted)

    async def generate_response(
        self,
        user_message: str,
        products: list,
        context: str
    ) -> str:
        """
        Genera una respuesta a partir de un mensaje de usuario y productos disponibles.
        """

        try:
            products_text = self.format_products_info(products[:20])

            prompt = f"""
                    Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
                    Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.

                    PRODUCTOS DISPONIBLES:
                    {products_text}

                    INSTRUCCIONES:
                    - Sé amigable y profesional
                    - Usa el contexto de la conversación anterior
                    - Recomienda productos específicos cuando sea apropiado
                    - Menciona precios, tallas y disponibilidad
                    - Si no tienes información, sé honesto

                    HISTORIAL DE CONVERSACIÓN:
                    {context}

                    Usuario: {user_message}

                    Asistente:
                    """

            response = await self.model.generate_content_async(prompt)

            if not response or not response.text:
                return "Lo siento, no puede generar una respuesta en este momento."

            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"Error en GeminiService: {str(e)}")