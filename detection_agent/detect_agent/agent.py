import os
import dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core.chat_engine import SimpleChatEngine
from typing import Dict

# Cargar las variables de entorno desde .env
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Verificar que la clave API esté cargada correctamente
assert OPENAI_API_KEY, "La clave API de OpenAI no está configurada."

class LLMAgent:
    def __init__(self):
        """
        Inicializa el agente LLM utilizando un modelo GPT (GPT-3.5 o GPT-4).
        """
        # Configura el LLM usando OpenAI y ajusta la temperatura a 0 para respuestas más determinísticas
        self.llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0.0)
        self.chat_engine = SimpleChatEngine.from_defaults(llm=self.llm)
        
        # Configura el motor de chat simple
        self.chat_engine = SimpleChatEngine.from_defaults(llm=self.llm)
        
    def detect_intent(self, query: str) -> str:
        """
        Enviar una consulta al motor de chat y obtener la intención detectada.
        """
        try:
            # Mensaje del sistema que guía al modelo a detectar la intención
            system_message = {
                "role": "system",
                "content": (
                    "Eres un asistente de soporte técnico especializado en detectar intenciones en la conversación del usuario. Tu tarea es devolver solo la intención del usuario en una palabra o frase corta"
                )
            }
            
            # Mensaje del usuario
            user_message = {
                "role": "user", 
                "content": f"mensaje a detectar: {query}"
            }
            combined_message = f"{system_message}\n\nMensaje a detectar: {query}"
            # Enviar los mensajes al motor de chat
            response = self.chat_engine.chat(combined_message)
            
            return response

        except Exception as e:
            return f"Error al detectar la intención: {e}"
    
    def chat(self, message: str) -> Dict[str, str]:
        """
        Envía un mensaje al agente y obtiene una respuesta.
        
        Args:
            message (str): El mensaje de entrada del usuario.
        
        Returns:
            dict: Un diccionario que contiene la respuesta del agente.
        """
        try:
            # Utiliza el motor de chat para interactuar con el LLM
            response = self.chat_engine.chat(message)
            # Formatear la respuesta como un diccionario para seguir la estructura
            return {"content": response}
        
        except Exception as e:
            print(f"Error al interactuar con el agente: {e}")
            return {
                "error": "No se pudo obtener una respuesta."
            }