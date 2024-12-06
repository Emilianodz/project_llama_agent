import requests
import json
import schedule
import time
import os

token = None

def update_token():
    global token
    url = "https://authconnectivity.qasar.app/api-auth/auth/singIn"

    payload = json.dumps({
    "email": os.getenv('EMAIL_QASAR_AGENT'),
    "password": os.getenv('PASSWORD_QASAR_AGENT')
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json()

    if response.status_code == 200:
        result = response.json().get('access_token')
        token = result
        print(f"Token actualizado exitosamente")
    else:
        print("Error al actualizar el token:", response.text)

    return token

# Ejecuta la función una vez de forma manual al inicio
initial_token = update_token()

# Programa la actualización automática
schedule.every(1).days.at("02:00").do(update_token)

# Bucle principal para mantener el programa en ejecución
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)