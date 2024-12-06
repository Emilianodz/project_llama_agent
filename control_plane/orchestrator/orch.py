import requests
import os
import dotenv
import logging
from llama_agents import (
    ControlPlaneServer,
    SimpleMessageQueue,
    AgentOrchestrator,
)
from llama_index.llms.openai import OpenAI

# Cargar las variables de entorno desde .env
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Asegurarse de que la API key esté disponible
if not OPENAI_API_KEY:
    raise ValueError("La clave API de OpenAI no está configurada correctamente.")

# Configurar el nivel de logging para ver el sistema trabajando
logging.getLogger("llama_agents").setLevel(logging.INFO)

# Configurar la cola de mensajes y el plano de control
message_queue = SimpleMessageQueue()

# Configurar el orquestador con el modelo de OpenAI
orchestrator = AgentOrchestrator(
    llm=OpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo", logprobs=None, default_headers={})
)

# Configurar el plano de control para orquestar los agentes conectados
control_plane = ControlPlaneServer(
    message_queue=message_queue,
    orchestrator=orchestrator,
)

# Función para interactuar con el orquestador y enviar el mensaje
def interact_with_agents(query: str) -> str:
    """
    Función que interactúa con el orquestador para enviar el mensaje y
    coordinar entre los diferentes agentes disponibles en el sistema.
    
    Args:
        query (str): Mensaje de entrada del usuario.
    
    Returns:
        str: Respuesta generada por el agente correspondiente.
    """
    # 1. LLAMADA AL MICROSERVICIO DE DETECCIÓN DE INTENCIÓN
    try:
        intent_response = requests.post("http://127.0.0.1:8001/detection_agent/", json={"query": query})
        if intent_response.status_code != 200:
            return "Error en el servicio de detección de intenciones"
        
        intent = intent_response.json().get("intent", "unknown")
        print(f"Intención detectada: {intent}")
        #return f"Intent detected: '{intent}'"
    
    except Exception as e:
        return f"Error en la interacción con el orquestador: {e}"
        
    
    # 2. LLAMADA AL MICROSERVICIO DE PLANIFICACIÓN DE ACCIONES 
    try:
        print(query)
        action_response = requests.post("http://127.0.0.1:8002/action_agent/", json={"query": query})
        print(action_response)
        if action_response.status_code != 200:
            return "Error en el servicio de ejecución de acciones"
        
        action = action_response.json().get("action", "unknown")
        print(f"Acción planificada: {action}")
        
        return f"Acción ejecutada: {action}"
    
    except requests.RequestException as e:
        return f"Error al contactar el servicio de ejecución de acciones: {e}"
        
        
    
