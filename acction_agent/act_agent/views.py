from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .agent import LLMAgent  # Importar la clase LLMAgent desde agent.py


# APIView para exponer la funcionalidad del agente a través de una API REST
@api_view(['POST'])
def action_agent(request):
    llm_agent = LLMAgent()  # Nueva instancia para cada solicitud
    query = request.data.get("query", "")
    if not query:
            return Response({"error": "No query provided"}, status=400)
        
    # Llamar al método process_query directamente en la clase LLMAgent
    response = llm_agent.process_query(query)
        
    # Devolver la respuesta en formato JSON
    return Response({"action": response}, status=status.HTTP_200_OK)
