from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .orch import interact_with_agents


# APIView para exponer la funcionalidad del agente a través de una API REST
@api_view(['POST'])
def orchestrator(request):
    query = request.data.get("query", "")
    if not query:
        return Response({"error": "No query provided"}, status=400)

    # Llamar al método process_query directamente en la clase LLMAgent
    response = interact_with_agents(query)

    # Devolver la respuesta final al cliente
    if isinstance(response, dict) and "error" in response:
        return Response({"error": response["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({"response": str(response)}, status=status.HTTP_200_OK)