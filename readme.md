# Proyecto de Agentes IA con LlamaIndex

Este proyecto consiste en una arquitectura de microservicios implementada en Django, que integra 4 agentes de IA diferentes utilizando LlamaIndex como herramienta principal.

## Descripción General

El sistema está compuesto por 4 proyectos principales:
1. action_agent - Agente que realiza acciones usando las apis de Qasar
2. detection_agent - Agente que detecta la intención del usuario
3. interaction_agent - Agente que interactúa con el usuario
4. controller - Controlador que coordina la interacción entre los agentes

## Arquitectura

La arquitectura es de microservicios, donde cada agente es un microservicio independiente que se comunica con el controlador para coordinar la interacción.

## Requisitos Previos

- Python
- Django 
- LlamaIndex
- Credenciales de OpenAI
- Credenciales de Qasar

## Instalación
1. Clonar el repositorio:

2. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   hay dos requirements.txt, uno general que espero que funcione para todos los proyectos y otro especifico para action_agent que si no funciona con el general, se debe usar el especifico, en caso de que sea necesario agregar mas dependencias, se debe agregar al requirements.txt general.
   ```

4. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   # En el proyecto se debe configurar las variables de entorno con las credenciales de OpenAI y Qasar, se usaban variables globales por lo que tal vez se requieran modificaciones para que sean variables de entorno.
   ```

## Estructura del Proyecto
![image](https://github.com/user-attachments/assets/fcb98cb5-cac8-4d3f-93d0-bfb914be1958)

