import openai
import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_info_by_iccid, increment_data_plan, get_id_by_email

# Configuración de OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

class LLMService:
    def __init__(self):
        # Inicializa cualquier valor necesario para la ejecución de funciones
        self.autogenerated_model_info = {}

    def incremento_plan_de_datos(self, email: str, iccid: str):
        """Llama a las funciones necesarias para incrementar el plan de datos."""
        try:
            # Obtener ID del usuario usando su correo electrónico
            user_info = get_id_by_email(email)
            self.autogenerated_model_info['companyClientId'] = user_info['companyClientId']
            self.autogenerated_model_info['userId'] = user_info['id']
            
            # Obtener información de la SIM usando el ICCID
            sim_info = get_info_by_iccid(iccid, self.autogenerated_model_info['companyClientId'])
            self.autogenerated_model_info['simId'] = sim_info['id']
            
            # Obtener información del plan de datos
            plan_info = plan_service_info(self.autogenerated_model_info['simId']).get('data', {})
            self.autogenerated_model_info.update({
                'annexId': plan_info.get('annexId'),
                'planId': plan_info.get('planId'),
                'planName': plan_info.get('planName'),
                'supplierId': plan_info.get('supplierId'),
                'idSupplierPlan': plan_info.get('idSupplierPlan'),
                'sku': plan_info.get('sku'),
                'serviceTime': plan_info.get('serviceTime'),
                'mb': plan_info.get('mb')
            })
            
            # Verifica si todos los datos requeridos están presentes
            if all(self.autogenerated_model_info[key] is not None for key in [
                'simId', 'annexId', 'planId', 'planName', 'supplierId', 'idSupplierPlan',
                'mb', 'sku', 'serviceTime', 'userId'
            ]):
                # Llama a la función para incrementar el plan de datos
                resultado = increment_data_plan(
                    int(self.autogenerated_model_info['simId']),
                    int(self.autogenerated_model_info['annexId']),
                    int(self.autogenerated_model_info['planId']),
                    str(self.autogenerated_model_info['planName']),
                    int(self.autogenerated_model_info['supplierId']),
                    int(self.autogenerated_model_info['idSupplierPlan']),
                    int(self.autogenerated_model_info['mb']),
                    str(self.autogenerated_model_info['sku']),
                    int(self.autogenerated_model_info['serviceTime']),
                    int(self.autogenerated_model_info['userId'])
                )
                return resultado
            else:
                return "No se pudo incrementar el plan de datos. Faltan datos necesarios."
        
        except Exception as e:
            return f"Error al intentar aumentar el plan de datos: {str(e)}"