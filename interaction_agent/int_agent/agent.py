import os
import dotenv
import requests
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
        self.llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0.0)
        self.chat_engine = SimpleChatEngine.from_defaults(llm=self.llm)
        
        # Inicializamos las variables para almacenar el historial de la conversación
        self.iccid = None
        self.email = None
        self.company_id = None

    def request_iccid(self, conversation_history: str) -> str:
        """
        Verificar si el ICCID ya está en el historial de la conversación, de lo contrario solicitarlo.
        """
        # Verificar si el ICCID ha sido proporcionado en el historial de la conversación
        if "ICCID" in conversation_history:
            # Extraer el ICCID del historial (suponiendo que esté en la forma 'ICCID: 123456789')
            self.iccid = conversation_history.split("ICCID:")[-1].split()[0].strip()
            return f"ICCID detectado: {self.iccid}"
        else:
            return "Por favor, proporcione su ICCID para proceder con la actualización de su plan de datos."

    def get_plan_details(self, iccid: str) -> Dict[str, str]:
        """
        Consultar el plan de datos disponible para el ICCID proporcionado.
        """
        try:
            # Llamar al endpoint de consulta de plan de datos (esto es solo un ejemplo)
            response = requests.post("http://localhost:8004/get_plan_details", json={"iccid": iccid})
            
            if response.status_code != 200:
                return {"error": "Error al consultar el plan de datos."}

            # Extraer la información del plan de datos
            plan_data = response.json()
            # Formatear el resultado
            return {
                "message": f"Su plan actual se actualizará a {plan_data['new_data_amount']} MB. ¿Desea proceder?"
            }
        
        except requests.RequestException as e:
            return {"error": f"Error en la solicitud al servidor: {e}"}

    def confirm_and_proceed(self, user_confirmation: str) -> str:
        """
        Confirmar si el usuario desea proceder con el aumento del plan de datos.
        """
        if user_confirmation.lower() == 'sí':
            # El usuario ha confirmado, por lo que necesitamos enviar el ICCID y el correo/company_id al orquestador
            if self.iccid and (self.email or self.company_id):
                # Llamar al orquestador para proceder con el aumento del plan
                try:
                    response = requests.post(
                        "http://localhost:8000/orchestrator", 
                        json={"iccid": self.iccid, "email": self.email, "company_id": self.company_id}
                    )
                    
                    if response.status_code == 200:
                        return "El aumento de su plan de datos ha sido exitosamente procesado."
                    else:
                        return "Hubo un problema al procesar su solicitud."

                except requests.RequestException as e:
                    return f"Error en la solicitud al orquestador: {e}"
            else:
                return "Falta información importante (ICCID, correo o company_id) para proceder."
        
        else:
            return "La operación fue cancelada por el usuario."

    def interact(self, query: str, conversation_history: str) -> str:
        """
        Manejar la interacción con el usuario para solicitar el ICCID, obtener el plan y proceder con la confirmación.
        """
        # Paso 1: Solicitar el ICCID si no está presente
        if not self.iccid:
            iccid_response = self.request_iccid(conversation_history)
            return iccid_response
        
        # Paso 2: Consultar el plan de datos disponible
        plan_response = self.get_plan_details(self.iccid)
        if "error" in plan_response:
            return plan_response["error"]
        
        # Paso 3: Solicitar la confirmación del usuario
        return plan_response["message"]
