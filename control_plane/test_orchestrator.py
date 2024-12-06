import unittest
from unittest.mock import patch
from orchestrator.orch import interact_with_agents

class OrchestratorTestCase(unittest.TestCase):
    
    @patch('orch.ControlPlaneServer.send_message')  # Mockear la función send_message
    def test_orchestrator_success(self, mock_send_message):
        # Simular una respuesta exitosa del microservicio
        mock_send_message.return_value = "Intent detected: 'aumentar plan de datos', Action executed."

        # Ejecutar la función que interactúa con el orquestador
        response = interact_with_agents("Quiero aumentar mi plan de datos")

        # Asegurarse de que el orquestador devuelve la respuesta correcta
        self.assertIn("Intent detected", response)
        self.assertIn("Action executed", response)

    @patch('orch.ControlPlaneServer.send_message')  # Mockear la función send_message
    def test_orchestrator_failure(self, mock_send_message):
        # Simular una respuesta de error
        mock_send_message.side_effect = Exception("Microservice failure")

        # Ejecutar la función que interactúa con el orquestador
        response = interact_with_agents("Quiero soporte técnico")

        # Verificar que el orquestador maneja el error correctamente
        self.assertIn("Error en la interacción con el orquestador", response)


if __name__ == "__main__":
    unittest.main()
