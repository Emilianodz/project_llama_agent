import requests
import urllib.parse
import json
from .api_tools import token

auth_token = token

def sent_auth_user(email, password):
    url = "https://authconnectivity.qasar.app/api-auth/auth/singIn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "email": email,
        "password": password
    }
    print(f"Enviando datos a la API: {data}")
    
    try:
        print(f"Enviando datos de autenticación: {data}")
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            print("Respuesta recibida exitosamente.")
            return response.json()  # if response is JSON
        else:
            print(f"Error en la solicitud. Código de estado: {response.status_code}")
            return {
                "error": "Error en la solicitud",
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            }
    except requests.exceptions.RequestException as e:
        print(f"Excepción al realizar la solicitud: {str(e)}")
        return {
            "error": "Excepción al realizar la solicitud",
            "exception": str(e)
        }

def get_id_by_email(email):
    encoded_email = urllib.parse.quote(email)
    url = f"https://authconnectivity.qasar.app/api-auth/users/getUserByEmail?email={encoded_email}"
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": "Error en la solicitud",
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "error": "Excepción al realizar la solicitud",
            "exception": str(e)
        }

def get_ICCID_by_id(user_id):
    url = f"https://simconnectivity.qasar.app/api/v1/reports/sims/{user_id}"
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Filtrar y devolver solo los datos relacionados con "iccid"
            details = data.get("detail", [])
            iccids = [item['iccid'] for item in details if 'iccid' in item]
            return {"iccids": iccids}
        else:
            return {
                "error": "Error en la solicitud",
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "error": "Excepción al realizar la solicitud",
            "exception": str(e)
        }

def get_info_by_id(sim_id, client_id):
    url = f"https://simconnectivity.qasar.app/api/v1/connectivity/sims/details/sim?id={sim_id}&clientId={client_id}"
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": "Error en la solicitud",
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "error": "Excepción al realizar la solicitud",
            "exception": str(e)
        }

# Nueva función: get_info_by_iccid
def get_info_by_iccid(iccid, companyClientId):
    url = f"https://simconnectivity.qasar.app/api/v1/connectivity/sims/details/sim?iccid={iccid}&clientId={companyClientId}"
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/xml'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": "Error en la solicitud",
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "error": "Excepción al realizar la solicitud",
            "exception": str(e)
        }


def get_data_sim_used(iccid):
    global auth_token
    url = f"https://simconnectivity.qasar.app/api/v1/connectivity/stats/{iccid}"
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("Respuesta recibida exitosamente.")
            return response.json()
        else:
            print(f"Error en la solicitud. Código de estado: {response.status_code}")
            return {
                "error": "Error en la solicitud",
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            }
    except requests.exceptions.RequestException as e:
        print(f"Excepción al realizar la solicitud: {str(e)}")
        return {
            "error": "Excepción al realizar la solicitud",
            "exception": str(e)
        }
        
def reset_sim(iccid):
    url = f"https://simconnectivity.qasar.app/api/v1/connectivity/reset/{iccid}"
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    try:
        response = requests.patch(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": "Error en la solicitud",
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "error": "Excepción al realizar la solicitud",
            "exception": str(e)
        }
        
def get_idsim_verification(iccid, page=1, items=100, status=1):
    url = f"https://simconnectivity.qasar.app/api/v1/connectivity/sims?page={page}&items={items}&status={status}&iccid={iccid}"
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": "Error en la solicitud",
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "error": "Excepción al realizar la solicitud",
            "exception": str(e)
        }
        
def plan_service_info(service_id):
    url = f"https://simconnectivity.qasar.app/api/v1/service/increment/{service_id}"
    headers = {
        'Authorization': f'Bearer {auth_token}' 
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return {
                "data": data
                }
            
        else:
            return {
                "error": "Error en la solicitud",
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "error": "Excepción al realizar la solicitud",
            "exception": str(e)
        }
        
def increment_data_plan(sim_id, annex_id, plan_id, plan_name, supplier_id, id_supplier_plan, mb, sku, service_time, user_id):
    url = "https://simconnectivity.qasar.app/api/v1/lines/increments"
    payload = json.dumps({
        "simId": sim_id,
        "newPlan": {
            "annexId": annex_id,
            "planId": plan_id,
            "planName": plan_name,
            "supplierId": supplier_id,
            "idSupplierPlan": id_supplier_plan,
            "mb": mb,
            "sku": sku,
            "serviceTime": service_time
        },
        "userId": user_id
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    response = requests.patch(url, headers=headers, data=payload)
    return response.json()